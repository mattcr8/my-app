from flask import Flask, render_template, jsonify
import requests
import os
from model import predict_goal

app = Flask(__name__)

API_KEY = os.environ.get("ODDS_API_KEY")

def get_odds():
    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"

    try:
        response = requests.get(url)
        data = response.json()

        odds_data = {}

        for match in data:
            home = match["home_team"]
            away = match["away_team"]

            bookmakers = match.get("bookmakers", [])

            odds = []

            for book in bookmakers:
                for market in book["markets"]:
                    for outcome in market["outcomes"]:
                        odds.append(outcome["price"])

            if odds:
                odds_data[f"{home}-{away}"] = max(odds)

        return odds_data

    except:
        return {}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/matches")
def matches():

    matches = [
        {"home":"Real Madrid","away":"Barcelona","minute":55,"shots":10,"xg":2.1,"score":"1-1"},
        {"home":"PSG","away":"Marseille","minute":60,"shots":12,"xg":2.5,"score":"2-0"},
        {"home":"Liverpool","away":"Chelsea","minute":30,"shots":5,"xg":0.8,"score":"0-0"}
    ]

    odds_data = get_odds()

    for m in matches:
        prob = predict_goal(m["xg"], m["shots"], m["minute"])

        key = f"{m['home']}-{m['away']}"
        best_odds = odds_data.get(key, 2.0)

        implied = 1 / best_odds
        real_prob = prob / 100

        value = round(real_prob / implied, 2)

        if value > 1.25:
            decision = "🔥 STRONG BET"
        elif value > 1.05:
            decision = "⚠️ MEDIUM BET"
        else:
            decision = "❌ NO BET"

        m["prob"] = prob
        m["decision"] = decision
        m["best_odds"] = best_odds
        m["value"] = value

    return jsonify(matches)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)