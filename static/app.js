async function loadMatches() {
    const res = await fetch("/matches");
    const data = await res.json();

    const container = document.getElementById("matches");
    container.innerHTML = "";

    data.forEach(m => {
        const div = document.createElement("div");

        div.className = "card " + (m.decision === "NEXT GOAL" ? "green" : "red");

        div.innerHTML = `
            <h2>${m.home} vs ${m.away}</h2>
            <p>Score: ${m.score}</p>
            <p>Minute: ${m.minute}</p>
            <p>Shots: ${m.shots}</p>
            <p>xG: ${m.xg}</p>

            <h3>${m.decision}</h3>

            <p>Probability: ${m.prob}%</p>
            <p>Odds: ${m.best_odds}</p>
            <p>Value: ${m.value}</p>
        `;

        container.appendChild(div);
    });
}

// 🔥 IMPORTANT : UNE SEULE FOIS AU LOAD
loadMatches();