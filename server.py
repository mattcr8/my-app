from flask import Flask, jsonify, render_template

app = Flask(__name__)

def generate_matches():
    return [
        {
            "home": "Real Madrid",
            "away": "Barcelona",
            "score": "1-1",
            "minute": 55,
            "shots": "10-8",
            "xg": 2.1,
            "prob": 82,
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
            "prob": 88,
            "decision": "NEXT GOAL",
            "confidence": 90,
            "reason": "Dominating game"
        },
        {
            "home": "Liverpool",
            "away": "Chelsea",
            "score": "0-0",
            "minute": 30,
            "shots": "5-4",
            "xg": 0.8,
            "prob": 45,
            "decision": "NO BET",
            "confidence": 40,
            "reason": "Low intensity"
        }
    ]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/matches")
def matches():
    return jsonify(generate_matches())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)