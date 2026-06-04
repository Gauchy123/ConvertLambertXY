from flask import Flask, request, jsonify
from pyproj import Transformer

app = Flask(__name__)

# Lambert ↔ WGS84
to_wgs84 = Transformer.from_crs("EPSG:26191", "EPSG:4326", always_xy=True)
to_lambert = Transformer.from_crs("EPSG:4326", "EPSG:26191", always_xy=True)

# Existing endpoint (keep it)
@app.route("/convert", methods=["POST"])
def convert():
    data = request.json

    x = float(data["x"])
    y = float(data["y"])

    lon, lat = to_wgs84.transform(x, y)

    return jsonify({
        "lat": lat,
        "lng": lon
    })

# NEW endpoint (add this)
@app.route("/reverse", methods=["POST"])
def reverse():
    data = request.json

    lat = float(data["lat"])
    lon = float(data["lng"])

    x, y = to_lambert.transform(lon, lat)

    return jsonify({
        "x": x,
        "y": y
    })

@app.route("/")
def home():
    return "API running"

if __name__ == "__main__":
    app.run()
