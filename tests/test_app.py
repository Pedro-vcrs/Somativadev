import json
import pytest
from app import app, get_weather

# --------- 
def test_home_route():
    client = app.test_client()
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"ClimaAgora API" in resp.data

def test_weather_valid_city(monkeypatch):
    
    monkeypatch.setattr("app.get_weather", lambda city: {
        "temperature": 25.5,
        "windspeed": 10,
        "time": "2025-09-21T12:00"
    })
    client = app.test_client()
    resp = client.get("/weather/Curitiba")
    data = json.loads(resp.data)
    assert resp.status_code == 200
    assert data["cidade"] == "Curitiba"
    assert "temperatura" in data
    assert "vento_kmh" in data

def test_weather_invalid_city(monkeypatch):
    monkeypatch.setattr("app.get_weather", lambda city: None)
    client = app.test_client()
    resp = client.get("/weather/NoPlace")
    assert resp.status_code == 404
    data = json.loads(resp.data)
    assert "error" in data


def test_get_weather_keys(monkeypatch):
    sample = {"current_weather": {"temperature": 20, "windspeed": 5, "time": "t"}}
    monkeypatch.setattr("requests.get", lambda *a, **k: type("R",(object,),{"json":lambda s=sample: sample})())
    
    def fake_geo(url, timeout=10):
        if "geocoding" in url:
            return type("R",(object,),{"json":lambda s={"results":[{"latitude":1,"longitude":1}]}: s})()
        return type("R",(object,),{"json":lambda s=sample: sample})()
    monkeypatch.setattr("requests.get", fake_geo)
    data = get_weather("Curitiba")
    assert set(["temperature","windspeed","time"]).issubset(data.keys())

def test_get_weather_no_results(monkeypatch):
   
    monkeypatch.setattr("requests.get", lambda *a, **k: type("R",(object,),{"json":lambda s={"results": []}: s})())
    assert get_weather("InvalidCity") is None
