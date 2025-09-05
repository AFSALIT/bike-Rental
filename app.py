from flask import Flask, jsonify, request, render_template
import firebase_admin
from firebase_admin import credentials, db

app = Flask(__name__, template_folder='templates')

# Initialize Firebase Realtime Database
cred = credentials.Certificate("bike-rendal-manage-firebase-adminsdk-fbsvc-a6d91a2ca6.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://bike-rendal-manage-default-rtdb.asia-southeast1.firebasedatabase.app/"   # 👈 replace with your Realtime DB URL
})

rentals_ref = db.reference("bike_rentals")


@app.route('/bike', methods=['GET', 'POST'])
def bike_rent():
    if request.method == 'POST':
        data = request.get_json()

        bike_number = str(data.get('bike_number', '')).strip()
        bike_name = str(data.get('bike_name', '')).strip()
        rent_start_date = str(data.get('rent_start_date', '')).strip()
        rent_end_date = str(data.get('rent_end_date', '')).strip()
        advance = data.get('advance', 0)
        full_cost = data.get('full_cost', 0)
        status = str(data.get('status', 'Booked'))

        # Validation
        if not bike_number or not bike_name or not rent_start_date or not rent_end_date:
            return jsonify({"error": "Missing required fields"}), 400

        # Normalize numeric fields
        def to_number(val):
            try:
                return float(val) if val not in (None, "") else 0
            except Exception:
                return 0

        rent_data = {
            "bike_number": bike_number,
            "bike_name": bike_name,
            "rent_start_date": rent_start_date,
            "rent_end_date": rent_end_date,
            "advance": to_number(advance),
            "full_cost": to_number(full_cost),
            "status": status
        }

        # Save data in Realtime DB (bike_number as key)
        try:
            rentals_ref.child(bike_number).set(rent_data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return jsonify({
            "message": "Bike rent details added successfully",
            "data": rent_data
        }), 201

    else:  # GET → return all rentals
        rentals = rentals_ref.get() or {}
        if isinstance(rentals, dict):
            rentals_list = list(rentals.values())
        elif isinstance(rentals, list):
            rentals_list = rentals
        else:
            rentals_list = []
        return jsonify({"rentals": rentals_list}), 200


# ✅ Get a single bike rental by bike_number
@app.route('/bike/<bike_number>', methods=['GET'])
def get_rental(bike_number):
    rental = rentals_ref.child(bike_number).get()
    if rental:
        return jsonify(rental), 200
    return jsonify({"error": "Bike rental not found"}), 404


# ✅ Update rental status or details
@app.route('/bike/<bike_number>', methods=['PUT'])
def update_rental(bike_number):
    data = request.get_json()
    rentals_ref.child(bike_number).update(data)
    return jsonify({"message": "Bike rental updated successfully"}), 200


# ✅ Delete a rental record
@app.route('/bike/<bike_number>', methods=['DELETE'])
def delete_rental(bike_number):
    rentals_ref.child(bike_number).delete()
    return jsonify({"message": "Bike rental deleted successfully"}), 200


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


if __name__ == '__main__':
    app.run(debug=True)
