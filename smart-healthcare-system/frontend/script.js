const VITAL_LABELS = {
  heart_rate: { label: "Heart Rate", unit: "bpm" },
  systolic_bp: { label: "Systolic BP", unit: "mmHg" },
  diastolic_bp: { label: "Diastolic BP", unit: "mmHg" },
  oxygen_saturation: { label: "SpO2", unit: "%" },
  temperature_c: { label: "Temperature", unit: "°C" },
};

const vitalsGrid = document.getElementById("vitals-grid");
const patientIdEl = document.getElementById("patient-id");
const badge = document.getElementById("anomaly-badge");
const logList = document.getElementById("log-list");

function renderVitals(reading, forecast, isAnomaly) {
  vitalsGrid.innerHTML = "";
  Object.keys(VITAL_LABELS).forEach((key) => {
    const { label, unit } = VITAL_LABELS[key];
    const value = reading[key];
    const predicted = forecast[key];

    const card = document.createElement("div");
    card.className = "vital-card" + (isAnomaly ? " flagged" : "");

    card.innerHTML = `
      <h4>${label}</h4>
      <div class="value">${value} <span style="font-size:0.9rem;color:#64748b;">${unit}</span></div>
      <div class="forecast">${predicted !== null ? `Trend forecast: ${predicted} ${unit}` : "Gathering trend data…"}</div>
    `;
    vitalsGrid.appendChild(card);
  });
}

function addLogEntry(reading, isAnomaly) {
  const li = document.createElement("li");
  const time = new Date(reading.timestamp * 1000).toLocaleTimeString();
  if (isAnomaly) {
    li.className = "anomaly-entry";
    li.textContent = `[${time}] Anomaly flagged for ${reading.patient_id} (tick ${reading.tick})`;
  } else {
    li.textContent = `[${time}] Reading OK for ${reading.patient_id} (tick ${reading.tick})`;
  }
  logList.prepend(li);
  while (logList.children.length > 30) logList.removeChild(logList.lastChild);
}

async function pollReading() {
  try {
    const res = await fetch("/api/reading");
    const data = await res.json();
    const { reading, anomaly, forecast } = data;

    patientIdEl.textContent = `Patient: ${reading.patient_id}`;
    badge.textContent = anomaly.is_anomaly ? "Anomaly Detected" : "Normal";
    badge.className = "badge " + (anomaly.is_anomaly ? "anomaly" : "normal");

    renderVitals(reading, forecast, anomaly.is_anomaly);
    addLogEntry(reading, anomaly.is_anomaly);
  } catch (err) {
    console.error("Failed to fetch reading:", err);
  }
}

pollReading();
setInterval(pollReading, 3000);
