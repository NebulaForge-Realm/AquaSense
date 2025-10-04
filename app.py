from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

# Store the latest ESP32 readings here
latest_data = {
    "id": 1,
    "lat": 28.6139,
    "lon": 77.2090,
    "temperature": None,
    "tds": None,
    "turbidity": None,
    "status": "No Data"
}

@app.route('/')
def index():
    return render_template('dashboard.html')

# 🔹 New route — ESP32 will send data here
@app.route('/upload', methods=['POST'])
def upload_data():
    global latest_data
    data = request.get_json()

    # If ESP32 sends JSON properly, store it
    if data:
        temp = data.get('temperature')
        tds = data.get('tds')
        turb = data.get('turbidity')

        # Compute status using same rules
        if temp > 32 or tds > 700 or turb > 40:
            status = "Unsafe"
        elif 24 <= temp <= 30 and 200 <= tds <= 500 and turb <= 25:
            status = "Safe"
        else:
            status = "Moderate"

        latest_data.update({
            "temperature": temp,
            "tds": tds,
            "turbidity": turb,
            "status": status
        })

        print("Received data:", latest_data)
        return jsonify({"message": "Data uploaded successfully!"}), 200
    else:
        return jsonify({"error": "No data received"}), 400

# 🔹 Dashboard requests latest data here
@app.route('/get_device')
def get_device():
    # If no real data yet, fallback to simulated
    if latest_data["temperature"] is None:
        temp = round(random.uniform(20, 35), 2)
        tds = round(random.uniform(100, 800), 2)
        turb = round(random.uniform(1, 50), 2)

        if temp > 32 or tds > 700 or turb > 40:
            status = "Unsafe"
        elif 24 <= temp <= 30 and 200 <= tds <= 500 and turb <= 25:
            status = "Safe"
        else:
            status = "Moderate"

        simulated_data = {
            "id": 1,
            "lat": 28.6139,
            "lon": 77.2090,
            "temperature": temp,
            "tds": tds,
            "turbidity": turb,
            "status": status
        }
        return jsonify(simulated_data)
    else:
        return jsonify(latest_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
