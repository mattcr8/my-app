from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

def advanced_ai(home, away, score, minute, shots, xg):

    shots_home, shots_away = map(int, shots.split("-"))
    goals_home, goals_away = map(int, score.split("-"))

    total_shots = shots_home + shots_away
    shot_diff = shots_home - shots_away
    goal_diff = goals_home - goals_away

    pressure = total_shots / max(1, minute)
    dominance = shot_diff * 0.5 + xg
    urgency = 1 if goal_diff == 0 else 0.7

    score_ai = (pressure * 30) + (dominance * 20) + (urgency * 10)
    score_ai += random.randint(-10, 10)

    prob = max(20, min(95, int(score_ai)))

    if prob > 70:
        decision = "NEXT GOAL"
        confidence = prob
    else:
        decision = "NO BET"
        confidence = prob

    return prob, decision, confidence


def generate_odds():
    return {
        "winamax": round(random.uniform(1.5, 3.0), 2),
        "betclic": round(random.uniform(1.5, 3.0), 2),
        "unibet": round(random.uniform(1.5, 3.0), 2),
    }


def calculate_value(prob, odds):
    best_odds = max(odds.values())
    value = (prob / 100 * best_odds) - 1
    return round(value, 2), best_odds


def generate_matches():
    base_matches = [
        ("Real Madrid", "Barcelona", "1-1", 55, "10-8", 2.1),
        ("PSG", "Marseille", "2-0", 60, "12-5", 2.5),
        ("Liverpool", "Chelsea", "0-0", 30, "5-4", 0.8),
    ]

    results = []

    for m in base_matches:

        prob, decision, confidence = advanced_ai(*m)
        odds = generate_odds()
        value, best_odds = calculate_value(prob, odds)

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
            "odds": odds,
            "best_odds": best_odds,
            "value": value
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