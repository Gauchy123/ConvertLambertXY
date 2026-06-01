from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import json

app = Flask(__name__)
CORS(app)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.json
        x = float(data["x"])
        y = float(data["y"])
        
        result = subprocess.run(
            ["python3", "-c", f"""
import pyproj
t = pyproj.Transformer.from_crs(4326, 26191, always_xy=True)
t2 = pyproj.Transformer.from_crs(26191, 4326, always_xy=True)
lon, lat = t2.transform({x}, {y})
print(f"{{lat}},{{lon}}")
"""],
            capture_output=True, text=True
        )
        lat, lon = result.stdout.strip().split(",")
        return jsonify({"lat": float(lat), "lng": float(lon)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Lambert API is running"

if __name__ == "__main__":
    app.run()
