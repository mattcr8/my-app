from flask import Flask, jsonify, render_template

app = Flask(__name__)

# IA simple basée sur stats
def analyze_match(home, away, score, minute, shots, xg):
    shots_home, shots_away = map(int, shots.split("-"))

    intensity = float(xg) + (shots_home + shots_away) / 10

    prob = min(95, max(30, int(intensity * 20)))

    if prob > 70:
        decision = "NEXT GOAL"
        confidence = min(95, prob)
        reason = "High pressure + strong xG"
    else:
        decision = "NO BET"
        confidence = prob
        reason = "Low intensity"

    return prob, decision, confidence, reason


def generate_matches():
    base_matches = [
        ("Real Madrid", "Barcelona", "1-1", 55, "10-8", 2.1),
        ("PSG", "Marseille", "2-0", 60, "12-5", 2.5),
        ("Liverpool", "Chelsea", "0-0", 30, "5-4", 0.8),
    ]

    results = []

    for m in base_matches:
        prob, decision, confidence, reason = analyze_match(*m)

        results.append({
            "home": m[0],
            "away": m[1],
            "score": m[2],
            "minute": m[3],
            "shots": m[4],
            "xg": m[5],
            "prob": prob,
            "decision": decision,
            "confidence": confidence,
            "reason": reason
        })

    return results


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/matches")
def matches():
    return jsonify(generate_matches())


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)