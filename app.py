from flask import Flask, render_template, jsonify
import random

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/get_device')
def get_device():
    # Simulated readings
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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


