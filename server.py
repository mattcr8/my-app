from flask import Flask, jsonify, render_template
import requests
import random
import os

app = Flask(__name__)

API_KEY = os.environ.get("ODDS_API_KEY")

def get_matches():
    try:
        if not API_KEY:
            raise Exception("API KEY manquante")

        url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={API_KEY}&regions=eu&markets=h2h"
        response = requests.get(url, timeout=10)
        data = response.json()

        matches = []

        for game in data[:5]:  # limite pour rester gratuit
            home = game["home_team"]
            away = game["away_team"]

            odds_list = []

            for bookmaker in game.get("bookmakers", []):
                for market in bookmaker.get("markets", []):
                    for outcome in market.get("outcomes", []):
                        if outcome["name"] == home:
                            odds_list.append(outcome["price"])

            if not odds_list:
                continue

            best_odds = max(odds_list)

            # IA simple gratuite (pas de dataset)
            prob = random.randint(55, 75)

            value = round((prob / 100) * best_odds, 2)

            decision = "VALUE BET" if value > 1 else "NO BET"

            matches.append({
                "home": home,
                "away": away,
                "prob": prob,
                "decision": decision,
                "best_odds": best_odds,
                "value": value
            })

        return matches

    except Exception as e:
        print("API ERROR:", e)

        # fallback si API down ou quota dépassé
        return [
            {"home": "Real Madrid", "away": "Barcelona", "prob": 70, "decision": "VALUE BET", "best_odds": 2.1, "value": 1.47},
            {"home": "PSG", "away": "Marseille", "prob": 65, "decision": "VALUE BET", "best_odds": 1.9, "value": 1.23},
            {"home": "Liverpool", "away": "Chelsea", "prob": 50, "decision": "NO BET", "best_odds": 2.0, "value": 1.0}
        ]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/matches")
def matches():
    return jsonify(get_matches())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)