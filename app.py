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


if __name__ == '__main__':
    app.run(debug=True)
