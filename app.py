from flask import Flask, jsonify, request, render_template, redirect, url_for
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__, template_folder='templates')

# Initialize Firebase Realtime Database
cred = credentials.Certificate("bike-rendal-manage-firebase-adminsdk-fbsvc-528aeea51d.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://bike-rendal-manage-default-rtdb.asia-southeast1.firebasedatabase.app/"   # 👈 replace with your Realtime DB URL
})

rentals_ref = db.reference("bike_rentals")
bikes_ref = db.reference("bikes")




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

        rental_data = {
            'bike_number': bike_number,
            'bike_name': bike_name,
            'rent_start_date': rent_start_date,
            'rent_end_date': rent_end_date,
            'advance': to_number(advance),
            'full_cost': to_number(full_cost),
            'commission': to_number(commission),
            'status': status,
            # Store optional fields as provided (empty string if not supplied)
            'renter_name': renter_name,
            'contact_no': contact_no
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
        # Ensure commission is handled as number
        if 'commission' in data:
            def to_number(val):
                try:
                    return float(val) if val not in (None, '') else 0
                except Exception:
                    return 0
            data['commission'] = to_number(data['commission'])
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

        if not bike_number or not date or not remark:
            return jsonify({"error": "Missing required fields"}), 400

        expense_data = {
            "bike_number": bike_number,
            "date": date,
            "remark": remark
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

if __name__ == '__main__':
    app.run(debug=True)
