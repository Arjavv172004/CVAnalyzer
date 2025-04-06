window.onload = async () => {
  const cursor = document.querySelector('.magic-cursor');
  document.addEventListener('mousemove', e => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
  });

  try {
    const res = await fetch('http://127.0.0.1:5000/jobs');
    const jobs = await res.json();

    const container = document.getElementById("job-container");

    jobs.forEach(job => {
      const card = document.createElement("div");
      card.className = "job-card";

      card.innerHTML = `
        <div class="job-title"><strong>${job}</strong></div>
        <button onclick="scanJob('${job}')">Scan</button>
      `;

      container.appendChild(card);
    });

  } catch (err) {
    document.getElementById("output").innerHTML = "❌ Failed to load jobs.";
  }
};

async function scanJob(job) {
  const output = document.getElementById("output");
  output.innerHTML = `🧠 Scanning CVs for <strong>${job}</strong>... Please wait`;

  try {
    const res = await fetch("http://127.0.0.1:5000/scan", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job })
    });

    const result = await res.json();

    if (result.shortlisted?.length > 0) {
      const list = result.shortlisted.map((c, index) => `
        <div class="shortlist-row">
          <div class="short-serial">#${index + 1}</div>
          <div class="short-id">${c.name}</div>
          <div class="short-email">${c.email}</div>
          <div class="short-score">${c.score}%</div>
        </div>
      `).join('');

      output.innerHTML = `
        <h3>✅ ${result.shortlisted.length} Candidate(s) Shortlisted for <strong>${job}</strong></h3>
        <div class="shortlist-table">${list}</div>
        <p>📧 Emails sent!</p>
      `;
    } else {
      output.innerHTML = `😕 No strong CVs matched for <strong>${job}</strong>.`;
    }
  } catch (error) {
    output.innerHTML = "❌ Error occurred while scanning.";
  }
}
