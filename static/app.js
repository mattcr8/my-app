async function fetchMatches() {
  try {
    const res = await fetch("/matches");
    const data = await res.json();

    console.log("DATA:", data); // 🔥 debug

    const container = document.getElementById("matches");

    if (!container) {
      console.error("DIV #matches introuvable");
      return;
    }

    container.innerHTML = "";

    data.forEach(match => {
      const div = document.createElement("div");

      const isBet = match.decision === "NEXT GOAL";
      div.className = "card " + (isBet ? "green" : "red");

      div.innerHTML = `
        <div class="title">${match.home} vs ${match.away}</div>
        <div>Score: ${match.score} | ${match.minute} min</div>
        <div class="stat">Shots: ${match.shots}</div>
        <div class="stat">xG: ${match.xg}</div>
        <div class="prob">Goal Probability: ${match.prob}%</div>
        <div class="${isBet ? "next" : "nobet"}">
          ${isBet ? "🔥 NEXT GOAL" : "❌ NO BET"}
        </div>
        <div>Confidence: ${match.confidence}%</div>
        <div>${match.reason}</div>
      `;

      container.appendChild(div);
    });

  } catch (error) {
    console.error("Erreur JS:", error);
  }
}

fetchMatches();
setInterval(fetchMatches, 5000);