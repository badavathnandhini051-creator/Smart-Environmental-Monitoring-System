from pathlib import Path
from datetime import datetime, timezone
import random

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(
    title="Smart Environmental Monitoring System",
    description="Beginner-friendly environmental monitoring demo with simulated sensor readings.",
    version="1.0.0",
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

# Demo mode: these values are simulated. No physical sensor is connected yet.
latest_reading = {
    "temperature_c": 27.4,
    "humidity_percent": 58.0,
    "source": "simulation",
    "timestamp": datetime.now(timezone.utc).isoformat(),
}

class SensorReading(BaseModel):
    temperature_c: float = Field(..., ge=-40, le=125)
    humidity_percent: float = Field(..., ge=0, le=100)
    source: str = Field(default="manual", max_length=30)

class Thresholds(BaseModel):
    temperature_max_c: float = Field(default=35, ge=-40, le=125)
    humidity_max_percent: float = Field(default=75, ge=0, le=100)

thresholds = Thresholds()

@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE_DIR / "static" / "index.html").read_text(encoding="utf-8")

@app.get("/health")
def health():
    return {"status": "ok", "message": "Monitoring API is running"}

@app.get("/api/reading")
def get_reading():
    return {**latest_reading, "alerts": make_alerts(latest_reading, thresholds)}

@app.post("/api/simulate")
def simulate_reading():
    """Create a new simulated temperature and humidity reading."""
    latest_reading.update({
        "temperature_c": round(random.uniform(20, 42), 1),
        "humidity_percent": round(random.uniform(30, 90), 1),
        "source": "simulation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return {**latest_reading, "alerts": make_alerts(latest_reading, thresholds)}

@app.post("/api/reading")
def submit_reading(reading: SensorReading):
    """Accept a reading from a sensor or a manual API request."""
    latest_reading.update({
        "temperature_c": reading.temperature_c,
        "humidity_percent": reading.humidity_percent,
        "source": reading.source,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    })
    return {**latest_reading, "alerts": make_alerts(latest_reading, thresholds)}

@app.get("/api/thresholds")
def get_thresholds():
    return thresholds.model_dump()

@app.put("/api/thresholds")
def update_thresholds(new_thresholds: Thresholds):
    global thresholds
    thresholds = new_thresholds
    return {"message": "Thresholds updated", **thresholds.model_dump()}

def make_alerts(reading, limits):
    alerts = []
    if reading["temperature_c"] > limits.temperature_max_c:
        alerts.append(f"High temperature: {reading['temperature_c']}°C is above {limits.temperature_max_c}°C.")
    if reading["humidity_percent"] > limits.humidity_max_percent:
        alerts.append(f"High humidity: {reading['humidity_percent']}% is above {limits.humidity_max_percent}%.")
    if not alerts:
        alerts.append("All readings are within the configured limits.")
    return alerts
