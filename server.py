from flask import Flask, jsonify, render_template

app = Flask(__name__)

data = [
    {
        "home": "Real Madrid",
        "away": "Barcelona",
        "score": "1-1",
        "minute": 55,
        "shots": "10-8",
        "xg": 2.1,
        "prob_goal": 95,
        "decision": "NEXT GOAL",
        "confidence": 90,
        "reason": "High pressure + strong xG"
    },
    {
        "home": "PSG",
        "away": "Marseille",
        "score": "2-0",
        "minute": 60,
        "shots": "12-5",
        "xg": 2.5,
        "prob_goal": 95,
        "decision": "NEXT GOAL",
        "confidence": 90,
        "reason": "PSG dominating"
    },
    {
        "home": "Liverpool",
        "away": "Chelsea",
        "score": "0-0",
        "minute": 30,
        "shots": "5-4",
        "xg": 0.8,
        "prob_goal": 42,
        "decision": "NO BET",
        "confidence": 40,
        "reason": "Low intensity"
    }
]

@app.route("/")
def home():
    return render_template("index.html", matches=data)

@app.route("/matches")
def matches():
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)