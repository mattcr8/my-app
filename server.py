from flask import Flask, jsonify

app = Flask(__name__)

def analyze_match(match):
    shots_home, shots_away = map(int, match["shots"].split("-"))
    total_shots = shots_home + shots_away

    # 🔥 INTENSITÉ (pression offensive)
    intensity = (total_shots * 2) + match["xg"] * 10

    # 🎯 PROBABILITÉ BUT (IA améliorée)
    prob_goal = min(95, int((match["xg"] * 30) + (total_shots * 2)))

    # 💰 FAKE ODDS (simulation bookmaker)
    odds = 1.5 if prob_goal > 80 else 2.0 if prob_goal > 65 else 2.5

    # 💰 VALUE BET
    value = round((prob_goal / 100 * odds) - 1, 2)

    # 🤖 DÉCISION IA
    if prob_goal > 80 and value > 0:
        decision = "NEXT GOAL"
        confidence = 90
        reason = "High pressure + strong xG"
    elif prob_goal > 65:
        decision = "WATCH"
        confidence = 65
        reason = "Moderate pressure"
    else:
        decision = "NO BET"
        confidence = 40
        reason = "Low intensity"

    return {
        **match,
        "intensity": int(intensity),
        "prob_goal": prob_goal,
        "odds": odds,
        "value": value,
        "decision": decision,
        "confidence": confidence,
        "reason": reason
    }

@app.route("/matches")
def matches():
    data = [
        {
            "home": "Real Madrid",
            "away": "Barcelona",
            "score": "1-1",
            "minute": 55,
            "shots": "10-8",
            "xg": 2.1
        },
        {
            "home": "PSG",
            "away": "Marseille",
            "score": "2-0",
            "minute": 60,
            "shots": "12-5",
            "xg": 2.5
        },
        {
            "home": "Liverpool",
            "away": "Chelsea",
            "score": "0-0",
            "minute": 30,
            "shots": "5-4",
            "xg": 0.8
        }
    ]

    analyzed = [analyze_match(m) for m in data]

    return jsonify(analyzed)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)