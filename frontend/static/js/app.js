let motionChart = null;

async function fetchClaims() {
  const res = await fetch("/api/claims");
  const claims = await res.json();
  const select = document.getElementById("claimSelect");
  select.innerHTML = "";
  claims.forEach(c => {
    const opt = document.createElement("option");
    opt.value = c.claim_id;
    opt.textContent = `${c.claim_id} (${c.label})`;
    select.appendChild(opt);
  });
}

async function fetchReport() {
  const select = document.getElementById("claimSelect");
  const claimId = select.value;
  if (!claimId) return;

  const res = await fetch(`/api/claim/${claimId}`);
  const report = await res.json();
  console.log("REPORT", report);
  renderReport(report);
}

function renderReport(report) {
  if (!report || !report.motion_signature || !report.cohesion) {
    console.error("Invalid report payload", report);
    return;
  }

  const ms = report.motion_signature;
  const coh = report.cohesion;
  const vf = report.video_facts || {};

  // Claim info line
  const infoDiv = document.getElementById("claimInfo");
  const label = vf.label || "unknown";
  const timing = vf.timing || "Unknown";
  const weather = vf.weather || "Unknown";
  infoDiv.textContent =
    `Claim: ${report.claim_id} · Type: ${label} · Time: ${timing} · Weather: ${weather}`;

  // Cohesion + timings
  const scoreDiv = document.getElementById("cohesionScore");
  const totalMs = report.timings ? report.timings.total_ms : null;
  scoreDiv.textContent =
    `Cohesion: ${coh.cohesion_score}/100` +
    (totalMs != null ? ` · ${totalMs} ms on-device` : "");

  scoreDiv.classList.remove("pill-green", "pill-orange", "pill-red");
  if (coh.cohesion_score > 70) {
    scoreDiv.classList.add("pill-green");
  } else if (coh.cohesion_score > 40) {
    scoreDiv.classList.add("pill-orange");
  } else {
    scoreDiv.classList.add("pill-red");
  }

  const alignDiv = document.getElementById("policeAlignment");
  alignDiv.textContent = `Police alignment: ${coh.police_alignment || "unknown"}`;

  // Contradictions
  const contrList = document.getElementById("contradictionsList");
  contrList.innerHTML = "";
  (coh.contradictions || []).forEach(item => {
    const li = document.createElement("li");
    li.textContent = `${item.fact}: ${item.status}`;
    if (item.status === "conflict") {
      li.style.color = "#feb2b2";
    }
    contrList.appendChild(li);
  });

  // What We Know
  const knowList = document.getElementById("whatWeKnowList");
  knowList.innerHTML = "";
  (coh.what_we_know || []).forEach(text => {
    const li = document.createElement("li");
    li.textContent = text;
    knowList.appendChild(li);
  });

  // Narrative drift
  document.getElementById("narrativeDrift").textContent =
    coh.narrative_drift || "";

  // AI summary + statements
  document.getElementById("aiSummary").textContent = report.ai_summary || "";
  document.getElementById("driverStatement").textContent =
    report.driver_statement || "";
  document.getElementById("policeSummary").textContent =
    report.police_summary || "";

  // Motion Signature chart
  const ctx = document.getElementById("motionChart").getContext("2d");
  const labels = (ms.timestamps || []).map(t => t.toFixed(2));
  const dataPoints = ms.risk || [];

  if (motionChart) {
    motionChart.destroy();
  }
  motionChart = new Chart(ctx, {
    type: "line",
    data: {
      labels,
      datasets: [{
        label: "Risk",
        data: dataPoints,
        borderColor: "#f56565",
        backgroundColor: "rgba(245,101,101,0.1)",
        fill: true,
        tension: 0.2
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false }
      },
      scales: {
        x: {
          title: { display: true, text: "Time (s)", color: "#e2e8f0" },
          ticks: { color: "#a0aec0" },
          grid: { color: "#2d3748" }
        },
        y: {
          title: { display: true, text: "Normalized risk", color: "#e2e8f0" },
          min: 0,
          max: 1,
          ticks: { color: "#a0aec0" },
          grid: { color: "#2d3748" }
        }
      }
    }
  });

  // Timeline
  const timelineDiv = document.getElementById("timeline");
  timelineDiv.innerHTML = "";
  const eventTime = ms.event_time_sec != null ? ms.event_time_sec.toFixed(2) : "N/A";
  const p = document.createElement("p");
  p.textContent = `Impact event around t = ${eventTime}s`;
  timelineDiv.appendChild(p);
}

window.addEventListener("DOMContentLoaded", async () => {
  await fetchClaims();
  document.getElementById("refreshBtn").addEventListener("click", fetchReport);
});
