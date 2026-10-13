# Smart Environmental Monitoring System

A beginner-friendly environmental monitoring prototype built with **Python, FastAPI, HTML, CSS, and JavaScript**. It displays temperature and humidity readings, lets users configure limits, and raises alerts when a reading exceeds those limits.

> **Current version is simulation-only.** It generates sample readings in software. No physical sensor or microcontroller is connected yet. Do not describe it as a hardware/IoT implementation until you build and test that part.

## Features

- Dashboard for the latest temperature and relative humidity
- Generate new simulated readings
- Configurable maximum temperature and humidity
- Alerts for values above configured limits
- REST API endpoints for health, readings, simulation, and thresholds
- Input validation using Pydantic
- Automated tests using pytest and FastAPI TestClient

## Technology stack

- Python 3.10+
- FastAPI — creates the backend API
- Uvicorn — runs the local development server
- HTML/CSS/JavaScript — browser dashboard
- Pytest + HTTPX — automated API tests

## Run on Windows

1. Install Python 3.10 or newer. During installation, select **Add Python to PATH**.
2. Extract this project ZIP.
3. Open the extracted `Smart-Environmental-Monitoring-System` folder in VS Code.
4. In VS Code, choose **Terminal → New Terminal**.
5. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

6. Activate it in PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this command for the current terminal only, then activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\.venv\Scripts\Activate.ps1
   ```

7. Install packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

8. Start the server:

   ```powershell
   python -m uvicorn app:app --reload
   ```

9. Open `http://127.0.0.1:8000` in your browser. Keep the terminal running.
10. API documentation is at `http://127.0.0.1:8000/docs`.

## Test the project

Open a second VS Code terminal in the project folder. Activate the environment if needed, then run:

```powershell
python -m pytest -q
```

The tests check the health endpoint, reading response, alert generation, invalid input, and threshold updates.

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check whether the API is running |
| GET | `/api/reading` | Get the latest reading and alerts |
| POST | `/api/simulate` | Generate a simulated reading |
| POST | `/api/reading` | Submit a sensor/manual reading |
| GET | `/api/thresholds` | Read alert limits |
| PUT | `/api/thresholds` | Update alert limits |

### Example: submit a reading

In `http://127.0.0.1:8000/docs`, open `POST /api/reading`, choose **Try it out**, and submit:

```json
{
  "temperature_c": 38,
  "humidity_percent": 82,
  "source": "manual-test"
}
```

Expected result: the response includes high-temperature and high-humidity alerts with the default limits.

## How it works

1. The browser requests the latest reading from `/api/reading`.
2. FastAPI returns the reading, its source, timestamp, and alerts.
3. The dashboard updates the displayed values.
4. The alert function compares the reading against the configured limits.
5. The tests send sample API requests and verify expected responses.

## Project structure

```text
Smart-Environmental-Monitoring-System/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

## Resume wording

Use this only after you have run the project and tested it:

**Smart Environmental Monitoring System | Python, FastAPI, REST APIs, HTML, CSS, JavaScript**
- Built a web-based prototype to monitor simulated temperature and humidity readings and flag values above configurable limits.
- Developed REST API endpoints with FastAPI for readings, threshold configuration, and alert generation.
- Added input validation and automated tests for API health, alert conditions, and invalid sensor values.

If you later connect an ESP32/Arduino and a real sensor, update the project description to state exactly which hardware you used and tested.

## Next improvements

- Connect a DHT11/DHT22 sensor to an ESP32 and send real readings to `/api/reading`.
- Store historical readings in SQLite or PostgreSQL.
- Add a graph of readings over time.
- Add alert notifications only after designing and testing a reliable notification mechanism.

## GitHub publishing

Create a **public** GitHub repository named `smart-environmental-monitoring-system`, then run these commands from this project folder:

```powershell
git init
git add .
git commit -m "Build environmental monitoring dashboard and API"
git branch -M main
git remote add origin https://github.com/YOUR-GITHUB-USERNAME/smart-environmental-monitoring-system.git
git push -u origin main
```

Replace `YOUR-GITHUB-USERNAME` with your actual GitHub username. If Git says a remote named `origin` already exists, check it with `git remote -v` before changing it.
