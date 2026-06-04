from flask import Flask, request, jsonify
from pyproj import Transformer

app = Flask(__name__)

# Lambert Maroc Nord ↔ WGS84
lambert_to_wgs84 = Transformer.from_crs(
    "EPSG:26191",
    "EPSG:4326",
    always_xy=True
)

wgs84_to_lambert = Transformer.from_crs(
    "EPSG:4326",
    "EPSG:26191",
    always_xy=True
)

@app.route("/")
def home():
    return "Lambert API is running"

# Lambert -> Lat/Lng
@app.route("/lambert-to-latlng", methods=["POST"])
def lambert_to_latlng():
    data = request.json

    x = float(data["x"])
    y = float(data["y"])

    lon, lat = lambert_to_wgs84.transform(x, y)

    return jsonify({
        "latitude": lat,
        "longitude": lon
    })

# Lat/Lng -> Lambert
@app.route("/latlng-to-lambert", methods=["POST"])
def latlng_to_lambert():
    data = request.json

    lat = float(data["latitude"])
    lon = float(data["longitude"])

    x, y = wgs84_to_lambert.transform(lon, lat)

    return jsonify({
        "x": x,
        "y": y
    })

if __name__ == "__main__":
    app.run()
