from flask import Flask, jsonify, render_template
import requests
import time
import random

app = Flask(__name__)

# 🔑 TES CLÉS API
ODDS_API_KEY = "TA_CLE_ODDS"
FOOTBALL_API_KEY = "TA_CLE_API_FOOTBALL"

# -----------------------------
# CACHE (économie crédits)
# -----------------------------
cache_data = None
cache_time = 0

# -----------------------------
# API FOOTBALL (matchs)
# -----------------------------
def get_matches():

    url = "https://v3.football.api-sports.io/fixtures?live=all"

    headers = {
        "x-apisports-key": FOOTBALL_API_KEY
    }

    res = requests.get(url, headers=headers)
    data = res.json()

    matches = []

    for m in data.get("response", [])[:5]:

        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]

        minute = m["fixture"]["status"]["elapsed"] or 0

        # FAKE stats (à améliorer plus tard)
        shots = f"{random.randint(3,12)}-{random.randint(3,12)}"
        xg = round(random.uniform(0.5, 2.5), 2)

        matches.append({
            "home": home,
            "away": away,
            "minute": minute,
            "shots": shots,
            "xg": xg
        })

    return matches


# -----------------------------
# API ODDS
# -----------------------------
def get_odds():

    url = f"https://api.the-odds-api.com/v4/sports/soccer_epl/odds/?apiKey={ODDS_API_KEY}&regions=eu&markets=h2h"

    res = requests.get(url)
    data = res.json()

    odds_map = {}

    for game in data[:10]:
        match_key = f"{game['home_team']} vs {game['away_team']}"

        odds = {}

        for b in game.get("bookmakers", []):
            name = b["title"].lower()

            if name in ["unibet", "betclic", "winamax"]:
                try:
                    odds[name] = b["markets"][0]["outcomes"][0]["price"]
                except:
                    pass

        if odds:
            odds_map[match_key] = odds

    return odds_map


# -----------------------------
# IA + VALUE
# -----------------------------
def analyze(match, odds):

    shots_home, shots_away = map(int, match["shots"].split("-"))
    total_shots = shots_home + shots_away

    pressure = total_shots / max(1, match["minute"])
    dominance = match["xg"]

    prob = min(95, max(20, int((pressure * 40) + (dominance * 20))))

    best_odds = max(odds.values())

    value = (prob / 100 * best_odds) - 1

    if value > 0:
        decision = "VALUE BET"
    else:
        decision = "NO BET"

    return prob, decision, round(value, 2), best_odds


# -----------------------------
# STACK COMPLET
# -----------------------------
def build_data():

    matches = get_matches()
    odds_map = get_odds()

    results = []

    for m in matches:

        key = f"{m['home']} vs {m['away']}"

        if key not in odds_map:
            continue

        odds = odds_map[key]

        prob, decision, value, best_odds = analyze(m, odds)

        results.append({
            "home": m["home"],
            "away": m["away"],
            "minute": m["minute"],
            "shots": m["shots"],
            "xg": m["xg"],
            "prob": prob,
            "decision": decision,
            "value": value,
            "odds": odds,
            "best_odds": best_odds
        })

    return results


# -----------------------------
# CACHE WRAPPER
# -----------------------------
def get_data_cached():
    global cache_data, cache_time

    if time.time() - cache_time < 60:
        return cache_data

    cache_data = build_data()
    cache_time = time.time()

    return cache_data


# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/matches")
def matches():
    return jsonify(get_data_cached())

# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)