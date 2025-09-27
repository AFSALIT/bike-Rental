from flask import Flask, jsonify, request, render_template, redirect, url_for, Response
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd
import openpyxl
import io

app = Flask(__name__, template_folder='templates')

# Initialize Firebase Realtime Database
cred = credentials.Certificate("bike-rendal-manage-firebase-adminsdk-fbsvc-737b987c79.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://bike-rendal-manage-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

rentals_ref = db.reference("bike_rentals")
bikes_ref = db.reference("bikes")
purchases_ref = db.reference("bike_purchases")
expenses_ref = db.reference("expenses")




# ✅ Serve frontend
@app.route('/')
def index():
    return render_template('index.html')

# New route for purchase bike
@app.route('/purchase-bike', methods=['GET', 'POST'])
def purchase_bike():
    if request.method == 'POST':
        data = request.form

        bike_name = str(data.get('bike_name', '')).strip()
        bike_number = str(data.get('bike_number', '')).strip()
        previous_owner_name = str(data.get('previous_owner_name', '')).strip()
        date = str(data.get('date', '')).strip()
        purchase_price = data.get('purchase_price', 0)
        condition = str(data.get('condition', '')).strip()

        # Validation
        if not bike_name or not bike_number or not previous_owner_name or not date or not purchase_price or not condition:
            return jsonify({"error": "Missing required fields"}), 400

        # Normalize numeric fields
        def to_number(val):
            try:
                return float(val) if val not in (None, "") else 0
            except Exception:
                return 0

        purchase_data = {
            "bike_name": bike_name,
            "bike_number": bike_number,
            "previous_owner_name": previous_owner_name,
            "date": date,
            "purchase_price": to_number(purchase_price),
            "condition": condition
        }

        # Save data in Realtime DB (bike_number as key)
        purchases_ref = db.reference("bike_purchases")
        try:
            purchases_ref.child(bike_number).set(purchase_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({
            "message": "Bike purchase details added successfully",
            "data": purchase_data
        }), 201

    else:  # GET → render the purchase bike form
        return render_template('purchase_bike.html')

# New API route to get list of purchase bikes
@app.route('/purchase-bike/list', methods=['GET'])
def list_purchase_bikes():
    purchases_ref = db.reference("bike_purchases")
    purchases = purchases_ref.get() or {}
    if isinstance(purchases, dict):
        purchases_list = list(purchases.values())
    elif isinstance(purchases, list):
        purchases_list = purchases
    else:
        purchases_list = []
    return jsonify({"purchases": purchases_list}), 200

# New API route to get a single purchase bike by bike_number
@app.route('/purchase-bike/<bike_number>', methods=['GET'])
def get_purchase_bike(bike_number):
    purchases_ref = db.reference("bike_purchases")
    purchase = purchases_ref.child(bike_number).get()
    if purchase:
        return jsonify(purchase), 200
    return jsonify({"error": "Purchase bike not found"}), 404

# New API route to update a purchase bike
@app.route('/purchase-bike/<bike_number>', methods=['PUT'])
def update_purchase_bike(bike_number):
    data = request.get_json()
    purchases_ref = db.reference("bike_purchases")
    try:
        purchases_ref.child(bike_number).update(data)
        return jsonify({"message": "Purchase bike updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New API route to delete a purchase bike
@app.route('/purchase-bike/<bike_number>', methods=['DELETE'])
def delete_purchase_bike(bike_number):
    purchases_ref = db.reference("bike_purchases")
    try:
        purchases_ref.child(bike_number).delete()
        return jsonify({"message": "Purchase bike deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ====== New: Bikes registry and per-bike rentals (Option 2) ======
@app.route('/bikes', methods=['GET', 'POST'])
def bikes_collection():
    if request.method == 'POST':
        data = request.get_json() or {}
        bike_number = str(data.get('bike_number', '')).strip()
        bike_name = str(data.get('bike_name', '')).strip()
        if not bike_number or not bike_name:
            return jsonify({'error': 'bike_number and bike_name are required'}), 400
        try:
            bikes_ref.child(bike_number).set({
                'bike_number': bike_number,
                'bike_name': bike_name
            })
            return jsonify({'message': 'Bike created', 'data': {'bike_number': bike_number, 'bike_name': bike_name}}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        bikes = bikes_ref.get() or {}
        if isinstance(bikes, dict):
            bikes_list = list(bikes.values())
        elif isinstance(bikes, list):
            bikes_list = bikes
        else:
            bikes_list = []
        return jsonify({'bikes': bikes_list}), 200

@app.route('/bikes/<bike_number>', methods=['GET', 'PUT', 'DELETE'])
def bikes_item(bike_number):
    if request.method == 'GET':
        bike = bikes_ref.child(bike_number).get()
        if not bike:
            return jsonify({'error': 'Bike not found'}), 404
        return jsonify(bike), 200
    elif request.method == 'PUT':
        data = request.get_json() or {}
        try:
            bikes_ref.child(bike_number).update(data)
            return jsonify({'message': 'Bike updated'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:  # DELETE
        try:
            # Optional: cascade delete rentals for this bike
            rentals_ref.child(bike_number).delete()
            bikes_ref.child(bike_number).delete()
            return jsonify({'message': 'Bike and its rentals deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Rentals under a specific bike
@app.route('/bikes/<bike_number>/rentals', methods=['GET', 'POST'])
def bike_rentals_collection(bike_number):
    # Ensure bike exists
    if not bikes_ref.child(bike_number).get():
        return jsonify({'error': 'Bike not found'}), 404

    if request.method == 'POST':
        data = request.get_json() or {}
        bike_name = str(data.get('bike_name', '')).strip()  # optional, for convenience
        rent_start_date = str(data.get('rent_start_date', '')).strip()
        rent_end_date = str(data.get('rent_end_date', '')).strip()
        advance = data.get('advance', 0)
        full_cost = data.get('full_cost', 0)
        commission = data.get('commission', 0)
        status = str(data.get('status', 'Booked')).strip()
        # New optional renter details
        renter_name = str(data.get('renter_name', '')).strip()
        contact_no = str(data.get('contact_no', '')).strip()

        if not rent_start_date or not rent_end_date:
            return jsonify({'error': 'rent_start_date and rent_end_date are required'}), 400

        def to_number(val):
            try:
                return float(val) if val not in (None, '') else 0
            except Exception:
                return 0

        # Separate commission into components
        total_commission = to_number(commission)
        platform_fee = total_commission * 0.6  # 60% platform fee
        service_charge = total_commission * 0.3  # 30% service charge
        other_fees = total_commission * 0.1  # 10% other fees

        rental_data = {
            'bike_number': bike_number,
            'bike_name': bike_name,
            'rent_start_date': rent_start_date,
            'rent_end_date': rent_end_date,
            'advance': to_number(advance),
            'full_cost': to_number(full_cost),
            'status': status,
            # Store optional fields as provided (empty string if not supplied)
            'renter_name': renter_name,
            'contact_no': contact_no,
            # Separated commission components
            'commission': {
                'platform_fee': platform_fee,
                'service_charge': service_charge,
                'other_fees': other_fees,
                'total_commission': total_commission
            }
        }
        try:
            new_ref = rentals_ref.child(bike_number).push(rental_data)
            rental_id = new_ref.key
            # Save id inside the record for convenience
            new_ref.update({'rental_id': rental_id})
            rental_data['rental_id'] = rental_id
            return jsonify({'message': 'Rental created', 'data': rental_data}), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        rentals = rentals_ref.child(bike_number).get() or {}
        if isinstance(rentals, dict):
            rentals_list = list(rentals.values())
        elif isinstance(rentals, list):
            rentals_list = rentals
        else:
            rentals_list = []
        return jsonify({'rentals': rentals_list}), 200

@app.route('/bikes/<bike_number>/rentals/<rental_id>', methods=['GET', 'PUT', 'DELETE'])
def bike_rentals_item(bike_number, rental_id):
    if request.method == 'GET':
        rental = rentals_ref.child(f"{bike_number}/{rental_id}").get()
        if not rental:
            return jsonify({'error': 'Rental not found'}), 404
        return jsonify(rental), 200
    elif request.method == 'PUT':
        data = request.get_json() or {}
        # Handle commission structure
        if 'commission' in data:
            if isinstance(data['commission'], (int, float)):
                # Handle legacy single commission value
                total_commission = float(data['commission'])
                data['commission'] = {
                    'platform_fee': total_commission * 0.6,
                    'service_charge': total_commission * 0.3,
                    'other_fees': total_commission * 0.1,
                    'total_commission': total_commission
                }
            elif isinstance(data['commission'], dict):
                # Handle new commission structure
                commission_data = data['commission']
                total_commission = (
                    commission_data.get('platform_fee', 0) +
                    commission_data.get('service_charge', 0) +
                    commission_data.get('other_fees', 0)
                )
                commission_data['total_commission'] = total_commission
                data['commission'] = commission_data

        try:
            rentals_ref.child(f"{bike_number}/{rental_id}").update(data)
            return jsonify({'message': 'Rental updated'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:  # DELETE
        try:
            rentals_ref.child(f"{bike_number}/{rental_id}").delete()
            return jsonify({'message': 'Rental deleted'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# Dashboard for Option 2
@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/expense', methods=['GET', 'POST'])
def expense():
    if request.method == 'POST':
        data = request.form
        bike_number = str(data.get('bike_number', '')).strip()
        date = str(data.get('date', '')).strip()
        remark = str(data.get('remark', '')).strip()
        amount = data.get('amount', 0)

        if not bike_number or not date or not remark:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate amount
        def to_number(val):
            try:
                return float(val) if val not in (None, "") else 0
            except Exception:
                return 0

        amount_value = to_number(amount)
        if amount_value <= 0:
            return jsonify({"error": "Amount must be a positive number"}), 400

        expense_data = {
            "bike_number": bike_number,
            "date": date,
            "remark": remark,
            "amount": amount_value
        }

        expenses_ref = db.reference("bike_expenses")
        try:
            new_ref = expenses_ref.push(expense_data)
            expense_id = new_ref.key
            new_ref.update({"id": expense_id})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({
            "message": "Expense added successfully",
            "data": expense_data
        }), 201
    else:
        return render_template('expense.html')

@app.route('/expense/list', methods=['GET'])
def list_expenses():
    expenses_ref = db.reference("bike_expenses")
    expenses = expenses_ref.get() or {}
    if isinstance(expenses, dict):
        expenses_list = list(expenses.values())
    elif isinstance(expenses, list):
        expenses_list = expenses
    else:
        expenses_list = []
    return jsonify({"expenses": expenses_list}), 200

@app.route('/expense/<expense_id>', methods=['GET'])
def get_expense(expense_id):
    expenses_ref = db.reference("bike_expenses")
    expense = expenses_ref.child(expense_id).get()
    if expense:
        return jsonify(expense), 200
    return jsonify({"error": "Expense not found"}), 404

@app.route('/expense/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    expenses_ref = db.reference("bike_expenses")
    try:
        expenses_ref.child(expense_id).delete()
        return jsonify({"message": "Expense deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New route for generating bike reports
@app.route('/report', methods=['GET'])
def generate_report():
    try:
        # Get all data from Firebase
        bikes_ref = db.reference("bikes")
        purchases_ref = db.reference("bike_purchases")
        rentals_ref = db.reference("bike_rentals")
        expenses_ref = db.reference("bike_expenses")

        bikes = bikes_ref.get() or {}
        purchases = purchases_ref.get() or {}
        rentals = rentals_ref.get() or {}
        expenses = expenses_ref.get() or {}

        report_data = []

        # Process each bike
        for bike_number, bike_data in bikes.items():
            # Get purchase data for this bike
            purchase_data = purchases.get(bike_number, {})
            purchase_price = purchase_data.get('purchase_price', 0)

            # Calculate total rental earnings for this bike
            bike_rentals = rentals.get(bike_number, {})
            total_rental_earning = 0
            total_commission = 0
            total_platform_fee = 0
            total_service_charge = 0
            total_other_fees = 0

            if isinstance(bike_rentals, dict):
                for rental in bike_rentals.values():
                    if isinstance(rental, dict):
                        total_rental_earning += float(rental.get('full_cost', 0))

                        # Handle commission calculation for both old and new structure
                        commission_data = rental.get('commission', {})
                        if isinstance(commission_data, dict):
                            # New structure
                            total_platform_fee += commission_data.get('platform_fee', 0)
                            total_service_charge += commission_data.get('service_charge', 0)
                            total_other_fees += commission_data.get('other_fees', 0)
                            total_commission += commission_data.get('total_commission', 0)
                        else:
                            # Old structure - single commission value
                            single_commission = float(commission_data or 0)
                            total_platform_fee += single_commission * 0.6
                            total_service_charge += single_commission * 0.3
                            total_other_fees += single_commission * 0.1
                            total_commission += single_commission

            # Calculate total expenses for this bike
            bike_expenses = []
            if isinstance(expenses, dict):
                bike_expenses = [
                    expense for expense in expenses.values()
                    if expense.get('bike_number') == bike_number
                ]

            total_expenses = sum(float(expense.get('amount', 0)) for expense in bike_expenses)

            # Add to report
            report_data.append({
                'bike_number': bike_number,
                'bike_name': bike_data.get('bike_name', purchase_data.get('bike_name', 'Unknown')),
                'purchase_price': purchase_price,
                'total_rental_earning': total_rental_earning,
                'total_expenses': total_expenses,
                'total_commission': total_commission,
                'platform_fee': total_platform_fee,
                'service_charge': total_service_charge,
                'other_fees': total_other_fees,
                'net_profit': total_rental_earning - total_expenses - purchase_price - total_commission
            })

        return jsonify({"report": report_data}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New route for downloading bike reports as Excel
@app.route('/report/download', methods=['GET'])
def download_report():
    try:
        # Get all data from Firebase
        bikes_ref = db.reference("bikes")
        purchases_ref = db.reference("bike_purchases")
        rentals_ref = db.reference("bike_rentals")
        expenses_ref = db.reference("bike_expenses")

        bikes = bikes_ref.get() or {}
        purchases = purchases_ref.get() or {}
        rentals = rentals_ref.get() or {}
        expenses = expenses_ref.get() or {}

        # Prepare data for DataFrame
        report_data = []

        # Process each bike
        for bike_number, bike_data in bikes.items():
            # Get purchase data for this bike
            purchase_data = purchases.get(bike_number, {})
            purchase_price = purchase_data.get('purchase_price', 0)

            # Calculate total rental earnings for this bike
            bike_rentals = rentals.get(bike_number, {})
            total_rental_earning = 0
            if isinstance(bike_rentals, dict):
                total_rental_earning = sum(
                    float(rental.get('full_cost', 0))
                    for rental in bike_rentals.values()
                )

            # Calculate total expenses for this bike
            bike_expenses = []
            if isinstance(expenses, dict):
                bike_expenses = [
                    expense for expense in expenses.values()
                    if expense.get('bike_number') == bike_number
                ]

            total_expenses = sum(float(expense.get('amount', 0)) for expense in bike_expenses)
            net_profit = total_rental_earning - total_expenses - purchase_price

            # Add to report data
            report_data.append({
                'Bike Number': bike_number,
                'Bike Name': bike_data.get('bike_name', purchase_data.get('bike_name', 'Unknown')),
                'Purchase Price ($)': purchase_price,
                'Total Rental Earning ($)': total_rental_earning,
                'Total Expenses ($)': total_expenses,
                'Net Profit ($)': net_profit
            })

        # Create DataFrame
        df = pd.DataFrame(report_data)

        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Bike Report', index=False)

            # Get the workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['Bike Report']

            # Format the header row
            header_font = openpyxl.styles.Font(bold=True, color="FFFFFF")
            header_fill = openpyxl.styles.PatternFill(start_color="4CAF50", end_color="4CAF50", fill_type="solid")

            for col_num, column_title in enumerate(df.columns, 1):
                cell = worksheet.cell(row=1, column=col_num)
                cell.font = header_font
                cell.fill = header_fill

            # Auto-adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 30)
                worksheet.column_dimensions[column_letter].width = adjusted_width

        output.seek(0)

        # Prepare response
        response = Response(
            output.getvalue(),
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={
                'Content-Disposition': 'attachment; filename=bike_report.xlsx'
            }
        )

        return response

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# New route for dashboard graph data
@app.route('/dashboard/graph-data', methods=['GET'])
def get_graph_data():
    try:
        # Get all data from Firebase
        bikes_ref = db.reference("bikes")
        purchases_ref = db.reference("bike_purchases")
        rentals_ref = db.reference("bike_rentals")
        expenses_ref = db.reference("bike_expenses")

        bikes = bikes_ref.get() or {}
        purchases = purchases_ref.get() or {}
        rentals = rentals_ref.get() or {}
        expenses = expenses_ref.get() or {}

        # 1. Bike Performance Comparison (Bar Chart)
        bike_performance = []
        for bike_number, bike_data in bikes.items():
            purchase_data = purchases.get(bike_number, {})
            purchase_price = purchase_data.get('purchase_price', 0)

            # Calculate total rental earnings for this bike
            bike_rentals = rentals.get(bike_number, {})
            total_rental_earning = 0
            if isinstance(bike_rentals, dict):
                total_rental_earning = sum(
                    float(rental.get('full_cost', 0))
                    for rental in bike_rentals.values()
                )

            # Calculate total expenses for this bike
            bike_expenses = []
            if isinstance(expenses, dict):
                bike_expenses = [
                    expense for expense in expenses.values()
                    if expense.get('bike_number') == bike_number
                ]

            total_expenses = sum(float(expense.get('amount', 0)) for expense in bike_expenses)
            net_profit = total_rental_earning - total_expenses - purchase_price

            bike_performance.append({
                'bike_number': bike_number,
                'bike_name': bike_data.get('bike_name', purchase_data.get('bike_name', 'Unknown')),
                'purchase_price': purchase_price,
                'rental_earning': total_rental_earning,
                'expenses': total_expenses,
                'net_profit': net_profit
            })

        # 2. Revenue Trends (Line Chart) - Monthly data for last 6 months
        revenue_trends = []
        from datetime import datetime, timedelta
        import calendar

        for i in range(5, -1, -1):  # Last 6 months
            date = datetime.now() - timedelta(days=i*30)
            month_name = calendar.month_name[date.month]
            year = date.year

            monthly_rentals = 0
            monthly_expenses = 0

            # Calculate monthly rentals
            if isinstance(rentals, dict):
                for bike_rentals_data in rentals.values():
                    if isinstance(bike_rentals_data, dict):
                        for rental in bike_rentals_data.values():
                            if isinstance(rental, dict):
                                rental_date = rental.get('rent_start_date', '')
                                if rental_date:
                                    try:
                                        rental_datetime = datetime.strptime(rental_date, '%Y-%m-%d')
                                        if rental_datetime.year == year and rental_datetime.month == date.month:
                                            monthly_rentals += float(rental.get('full_cost', 0))
                                    except:
                                        pass

            # Calculate monthly expenses
            if isinstance(expenses, dict):
                for expense in expenses.values():
                    if isinstance(expense, dict):
                        expense_date = expense.get('date', '')
                        if expense_date:
                            try:
                                expense_datetime = datetime.strptime(expense_date, '%Y-%m-%d')
                                if expense_datetime.year == year and expense_datetime.month == date.month:
                                    monthly_expenses += float(expense.get('amount', 0))
                            except:
                                pass

            revenue_trends.append({
                'month': f"{month_name} {year}",
                'rentals': monthly_rentals,
                'expenses': monthly_expenses,
                'profit': monthly_rentals - monthly_expenses
            })

        # 3. Rental Status Distribution (Pie Chart)
        status_counts = {'Booked': 0, 'Active': 0, 'Returned': 0, 'Cancelled': 0}
        if isinstance(rentals, dict):
            for bike_rentals_data in rentals.values():
                if isinstance(bike_rentals_data, dict):
                    for rental in bike_rentals_data.values():
                        if isinstance(rental, dict):
                            status = rental.get('status', 'Unknown')
                            if status in status_counts:
                                status_counts[status] += 1

        # 4. Expense Breakdown by Bike (Doughnut Chart)
        expense_breakdown = []
        for bike_number, bike_data in bikes.items():
            bike_expenses = []
            if isinstance(expenses, dict):
                bike_expenses = [
                    expense for expense in expenses.values()
                    if expense.get('bike_number') == bike_number
                ]

            total_expenses = sum(float(expense.get('amount', 0)) for expense in bike_expenses)
            if total_expenses > 0:
                expense_breakdown.append({
                    'bike_number': bike_number,
                    'bike_name': bike_data.get('bike_name', purchase_data.get('bike_name', 'Unknown')),
                    'expenses': total_expenses
                })

        # 5. Commission Breakdown by Type (Pie Chart)
        commission_by_type = {
            'platform_fee': 0,
            'service_charge': 0,
            'other_fees': 0
        }

        if isinstance(rentals, dict):
            for bike_rentals_data in rentals.values():
                if isinstance(bike_rentals_data, dict):
                    for rental in bike_rentals_data.values():
                        if isinstance(rental, dict):
                            commission_data = rental.get('commission', {})
                            if isinstance(commission_data, dict):
                                commission_by_type['platform_fee'] += commission_data.get('platform_fee', 0)
                                commission_by_type['service_charge'] += commission_data.get('service_charge', 0)
                                commission_by_type['other_fees'] += commission_data.get('other_fees', 0)
                            else:
                                # Handle legacy single commission value
                                single_commission = float(commission_data or 0)
                                commission_by_type['platform_fee'] += single_commission * 0.6
                                commission_by_type['service_charge'] += single_commission * 0.3
                                commission_by_type['other_fees'] += single_commission * 0.1

        return jsonify({
            "bike_performance": bike_performance,
            "revenue_trends": revenue_trends,
            "rental_status": status_counts,
            "expense_breakdown": expense_breakdown,
            "commission_breakdown": commission_by_type
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/bikes/available', methods=['GET'])
def available_bikes():
    try:
        bikes = bikes_ref.get() or {}
        rentals = rentals_ref.get() or {}
        available = []
        for bike_number, bike_data in bikes.items():
            bike_rentals = rentals.get(bike_number, {}) or {}
            has_current = False
            if isinstance(bike_rentals, dict):
                for rental in bike_rentals.values():
                    if isinstance(rental, dict):
                        status = str(rental.get('status', '')).strip()
                        if status in ('Booked', 'Active'):
                            has_current = True
                            break
            if not has_current:
                available.append({
                    'bike_number': bike_number,
                    'bike_name': bike_data.get('bike_name', '')
                })
        return jsonify({'available_bikes': available}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/bikes/<bike_number>/summary', methods=['GET'])
def bike_summary(bike_number):
    try:
        # Fetch bike details
        bike = bikes_ref.child(bike_number).get() or {}
        if not bike:
            return jsonify({'error': 'Bike not found'}), 404

        # Fetch rentals
        rentals = rentals_ref.child(bike_number).get() or {}
        rentals_list = list(rentals.values()) if isinstance(rentals, dict) else []

        # Fetch purchase
        purchase = purchases_ref.child(bike_number).get() or {}

        # Fetch expenses for this bike
        all_expenses = expenses_ref.get() or {}
        bike_expenses = []
        if isinstance(all_expenses, dict):
            for exp_id, exp_data in all_expenses.items():
                if isinstance(exp_data, dict) and exp_data.get('bike_number') == bike_number:
                    bike_expenses.append(exp_data)

        # Compute aggregates
        total_rentals = len(rentals_list)
        total_revenue = sum(float(r.get('full_cost', 0)) for r in rentals_list)
        total_advance = sum(float(r.get('advance', 0)) for r in rentals_list)

        # Commission breakdown
        platform_fee = sum(float(r.get('commission', {}).get('platform_fee', 0)) for r in rentals_list)
        service_charge = sum(float(r.get('commission', {}).get('service_charge', 0)) for r in rentals_list)
        other_fees = sum(float(r.get('commission', {}).get('other_fees', 0)) for r in rentals_list)
        total_commission = sum(float(r.get('commission', {}).get('total_commission', 0)) for r in rentals_list)

        # Status counts
        status_counts = {}
        for r in rentals_list:
            status = str(r.get('status', 'Unknown')).strip()
            status_counts[status] = status_counts.get(status, 0) + 1

        # Purchase and expenses
        purchase_price = float(purchase.get('purchase_price', 0))
        total_expenses = sum(float(e.get('amount', 0)) for e in bike_expenses)

        summary = {
            'bike_number': bike_number,
            'bike_name': bike.get('bike_name', ''),
            'total_rentals': total_rentals,
            'total_revenue': total_revenue,
            'total_advance': total_advance,
            'commissions': {
                'platform_fee': platform_fee,
                'service_charge': service_charge,
                'other_fees': other_fees,
                'total_commission': total_commission
            },
            'status_counts': status_counts,
            'purchase_price': purchase_price,
            'total_expenses': total_expenses,
            'net_profit': total_revenue - total_commission - total_expenses  # Simple net
        }

        return jsonify(summary), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/bikes/<bike_number>/report/download', methods=['GET'])
def download_bike_report(bike_number):
    try:
        # Reuse summary logic
        bike = bikes_ref.child(bike_number).get() or {}
        if not bike:
            return jsonify({'error': 'Bike not found'}), 404

        rentals = rentals_ref.child(bike_number).get() or {}
        rentals_list = list(rentals.values()) if isinstance(rentals, dict) else []

        purchase = purchases_ref.child(bike_number).get() or {}

        all_expenses = expenses_ref.get() or {}
        bike_expenses = []
        if isinstance(all_expenses, dict):
            for exp_id, exp_data in all_expenses.items():
                if isinstance(exp_data, dict) and exp_data.get('bike_number') == bike_number:
                    bike_expenses.append(exp_data)

        # Compute aggregates (same as summary)
        total_rentals = len(rentals_list)
        total_revenue = sum(float(r.get('full_cost', 0)) for r in rentals_list)
        total_advance = sum(float(r.get('advance', 0)) for r in rentals_list)

        platform_fee = sum(float(r.get('commission', {}).get('platform_fee', 0)) for r in rentals_list)
        service_charge = sum(float(r.get('commission', {}).get('service_charge', 0)) for r in rentals_list)
        other_fees = sum(float(r.get('commission', {}).get('other_fees', 0)) for r in rentals_list)
        total_commission = sum(float(r.get('commission', {}).get('total_commission', 0)) for r in rentals_list)

        status_counts = {}
        for r in rentals_list:
            status = str(r.get('status', 'Unknown')).strip()
            status_counts[status] = status_counts.get(status, 0) + 1

        purchase_price = float(purchase.get('purchase_price', 0))
        total_expenses = sum(float(e.get('amount', 0)) for e in bike_expenses)
        net_profit = total_revenue - total_commission - total_expenses

        # Create summary DataFrame
        summary_data = {
            'Metric': [
                'Bike Number', 'Bike Name', 'Total Rentals', 'Total Revenue', 'Total Advance',
                'Platform Fee', 'Service Charge', 'Other Fees', 'Total Commission',
                'Purchase Price', 'Total Expenses', 'Net Profit'
            ],
            'Value': [
                bike_number, bike.get('bike_name', ''), total_rentals, total_revenue, total_advance,
                platform_fee, service_charge, other_fees, total_commission,
                purchase_price, total_expenses, net_profit
            ]
        }
        summary_df = pd.DataFrame(summary_data)

        # Status counts row
        status_row = pd.DataFrame({
            'Metric': ['Status Counts'] + list(status_counts.keys()),
            'Value': [''] + list(status_counts.values())
        })
        summary_df = pd.concat([summary_df, status_row], ignore_index=True)

        # Create Excel file in memory
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Add rentals sheet if any
            if rentals_list:
                rentals_df = pd.DataFrame(rentals_list)
                rentals_df.to_excel(writer, sheet_name='Rentals', index=False)

            # Add expenses sheet if any
            if bike_expenses:
                expenses_df = pd.DataFrame(bike_expenses)
                expenses_df.to_excel(writer, sheet_name='Expenses', index=False)

        output.seek(0)

        filename = f"bike_summary_{bike_number}.xlsx"
        return Response(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# New route for commission breakdown data
@app.route('/dashboard/commission-breakdown', methods=['GET'])
def get_commission_breakdown():
    try:
        rentals_ref = db.reference("bike_rentals")
        rentals = rentals_ref.get() or {}

        # Commission breakdown by type
        commission_summary = {
            'platform_fee': 0,
            'service_charge': 0,
            'other_fees': 0,
            'total_commission': 0
        }

        # Commission trends over last 6 months
        commission_trends = []
        from datetime import datetime, timedelta
        import calendar

        for i in range(5, -1, -1):
            date = datetime.now() - timedelta(days=i*30)
            month_name = calendar.month_name[date.month]
            year = date.year

            monthly_commissions = {
                'platform_fee': 0,
                'service_charge': 0,
                'other_fees': 0,
                'total_commission': 0
            }

            if isinstance(rentals, dict):
                for bike_rentals_data in rentals.values():
                    if isinstance(bike_rentals_data, dict):
                        for rental in bike_rentals_data.values():
                            if isinstance(rental, dict):
                                # Handle both old and new commission structure
                                commission_data = rental.get('commission', {})
                                if isinstance(commission_data, dict):
                                    # New structure
                                    monthly_commissions['platform_fee'] += commission_data.get('platform_fee', 0)
                                    monthly_commissions['service_charge'] += commission_data.get('service_charge', 0)
                                    monthly_commissions['other_fees'] += commission_data.get('other_fees', 0)
                                    monthly_commissions['total_commission'] += commission_data.get('total_commission', 0)
                                else:
                                    # Old structure - single commission value
                                    single_commission = float(commission_data or 0)
                                    monthly_commissions['platform_fee'] += single_commission * 0.6
                                    monthly_commissions['service_charge'] += single_commission * 0.3
                                    monthly_commissions['other_fees'] += single_commission * 0.1
                                    monthly_commissions['total_commission'] += single_commission

                                # Check if rental date matches current month
                                rental_date = rental.get('rent_start_date', '')
                                if rental_date:
                                    try:
                                        rental_datetime = datetime.strptime(rental_date, '%Y-%m-%d')
                                        if rental_datetime.year == year and rental_datetime.month == date.month:
                                            # Commission already added above, no need to add again
                                            pass
                                    except:
                                        pass

            commission_trends.append({
                'month': f"{month_name} {year}",
                'platform_fee': monthly_commissions['platform_fee'],
                'service_charge': monthly_commissions['service_charge'],
                'other_fees': monthly_commissions['other_fees'],
                'total_commission': monthly_commissions['total_commission']
            })

            # Add to total summary
            commission_summary['platform_fee'] += monthly_commissions['platform_fee']
            commission_summary['service_charge'] += monthly_commissions['service_charge']
            commission_summary['other_fees'] += monthly_commissions['other_fees']
            commission_summary['total_commission'] += monthly_commissions['total_commission']

        return jsonify({
            "commission_summary": commission_summary,
            "commission_trends": commission_trends
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
