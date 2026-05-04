from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    matches = [
        {
            "home": "Real Madrid",
            "away": "Barcelona",
            "score": "1-1",
            "minute": 55,
            "shots": "10-8",
            "xg": 2.1,
            "decision": "NEXT GOAL"
        },
        {
            "home": "PSG",
            "away": "Marseille",
            "score": "2-0",
            "minute": 60,
            "shots": "12-5",
            "xg": 2.5,
            "decision": "NEXT GOAL"
        },
        {
            "home": "Liverpool",
            "away": "Chelsea",
            "score": "0-0",
            "minute": 30,
            "shots": "5-4",
            "xg": 0.8,
            "decision": "NO BET"
        }
    ]

    return render_template("index.html", matches=matches)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)