from flask import Flask, request, jsonify
from flask_cors import CORS
from pyproj import Transformer

app = Flask(__name__)
CORS(app)

transformer = Transformer.from_crs(
    "EPSG:26191", "EPSG:4326", always_xy=True
)

@app.route("/convert", methods=["POST"])
def convert():
    try:
        data = request.json
        x = float(data["x"])
        y = float(data["y"])
        lon, lat = transformer.transform(x, y)
        return jsonify({"lat": lat, "lng": lon})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/")
def home():
    return "Lambert API is running"

if __name__ == "__main__":
    app.run()
