const temperatureEl = document.getElementById("temperature");
const humidityEl = document.getElementById("humidity");
const sourceEl = document.getElementById("source");
const alertsEl = document.getElementById("alerts");
const timestampEl = document.getElementById("timestamp");
const connectionEl = document.getElementById("connection");
const formMessageEl = document.getElementById("formMessage");

function showAlerts(alerts) {
  alertsEl.replaceChildren();
  const isWarning = alerts.some((message) => !message.startsWith("All readings"));
  alertsEl.classList.toggle("warning", isWarning);
  alerts.forEach((message) => {
    const line = document.createElement("div");
    line.textContent = message;
    alertsEl.appendChild(line);
  });
}

async function loadReading() {
  try {
    const response = await fetch("/api/reading");
    if (!response.ok) throw new Error("Could not get reading");
    const data = await response.json();
    temperatureEl.textContent = Number(data.temperature_c).toFixed(1);
    humidityEl.textContent = Number(data.humidity_percent).toFixed(1);
    sourceEl.textContent = data.source;
    timestampEl.textContent = new Date(data.timestamp).toLocaleString();
    showAlerts(data.alerts);
    connectionEl.textContent = "API connected";
    connectionEl.style.background = "#dcfce7";
    connectionEl.style.color = "#166534";
  } catch (error) {
    connectionEl.textContent = "API disconnected";
    connectionEl.style.background = "#fee2e2";
    connectionEl.style.color = "#991b1b";
    alertsEl.textContent = "Could not reach the API. Check that the server is running.";
    alertsEl.classList.add("warning");
  }
}

document.getElementById("simulateButton").addEventListener("click", async () => {
  const button = document.getElementById("simulateButton");
  button.disabled = true;
  button.textContent = "Generating…";
  try {
    const response = await fetch("/api/simulate", { method: "POST" });
    if (!response.ok) throw new Error("Simulation failed");
    await loadReading();
  } catch (error) {
    formMessageEl.textContent = "Could not generate a reading. Is the server running?";
  } finally {
    button.disabled = false;
    button.textContent = "Generate new reading";
  }
});

document.getElementById("thresholdForm").addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    temperature_max_c: Number(document.getElementById("maxTemperature").value),
    humidity_max_percent: Number(document.getElementById("maxHumidity").value)
  };
  try {
    const response = await fetch("/api/thresholds", {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!response.ok) throw new Error("Invalid limits");
    formMessageEl.textContent = "Limits saved successfully.";
    await loadReading();
  } catch (error) {
    formMessageEl.textContent = "Could not save limits. Check the values and try again.";
  }
});

async function loadThresholds() {
  try {
    const response = await fetch("/api/thresholds");
    const data = await response.json();
    document.getElementById("maxTemperature").value = data.temperature_max_c;
    document.getElementById("maxHumidity").value = data.humidity_max_percent;
  } catch (_) {
    // The dashboard displays a connection warning if the API is unavailable.
  }
}

loadThresholds();
loadReading();
