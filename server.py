from flask import Flask, jsonify, render_template
import random

app = Flask(__name__)

# Fake data (remplacable par API plus tard)
def generate_matches():
    return [
        {
            "home": "Real Madrid",
            "away": "Barcelona",
            "score": "1-1",
            "minute": 55,
            "shots": "10-8",
            "xg": 2.1,
            "prob": random.randint(75, 95),
            "confidence": 90,
            "decision": "NEXT GOAL",
            "reason": "High pressure + strong xG"
        },
        {
            "home": "PSG",
            "away": "Marseille",
            "score": "2-0",
            "minute": 60,
            "shots": "12-5",
            "xg": 2.5,
            "prob": random.randint(80, 95),
            "confidence": 90,
            "decision": "NEXT GOAL",
            "reason": "Dominating game"
        },
        {
            "home": "Liverpool",
            "away": "Chelsea",
            "score": "0-0",
            "minute": 30,
            "shots": "5-4",
            "xg": 0.8,
            "prob": random.randint(30, 60),
            "confidence": 40,
            "decision": "NO BET",
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