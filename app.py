from flask import Flask, jsonify
import requests

app = Flask(__name__)

def get_weather(city):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    geo_resp = requests.get(geo_url, timeout=10).json()

    if "results" not in geo_resp or not geo_resp["results"]:
        return None

    lat = geo_resp["results"][0]["latitude"]
    lon = geo_resp["results"][0]["longitude"]

    weather_url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        "&current_weather=true"
    )
    weather_resp = requests.get(weather_url, timeout=10).json()
    return weather_resp.get("current_weather")

@app.route("/weather/<city>")
def weather(city):
    data = get_weather(city)
    if not data:
        return jsonify({"error": "Cidade não encontrada"}), 404
    return jsonify({
        "cidade": city,
        "temperatura": data["temperature"],
        "vento_kmh": data["windspeed"],
        "hora_observacao": data["time"]
    })

@app.route("/")
def home():
    return (
        "<h2>ClimaAgora API</h2>"
        "<p>Acesse /weather/&lt;Cidade&gt; para ver clima atual.<br>"
        "Exemplo: /weather/Florianopolis</p>"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
