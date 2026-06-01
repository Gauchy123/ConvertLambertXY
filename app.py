from flask import Flask, request, jsonify
from pyproj import Transformer

app = Flask(__name__)

# Lambert Maroc Nord (EPSG le plus utilisé)
transformer = Transformer.from_crs("EPSG:26191", "EPSG:4326", always_xy=True)

@app.route("/convert", methods=["POST"])
def convert():
    data = request.json

    x = float(data["x"])
    y = float(data["y"])

    lon, lat = transformer.transform(x, y)

    return jsonify({
        "lat": lat,
        "lng": lon
    })

@app.route("/")
def home():
    return "Lambert API is running"

if __name__ == "__main__":
    app.run()
