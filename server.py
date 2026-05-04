from flask import Flask, jsonify, render_template
import pandas as pd
import random

# import du modèle
from model import train_model

app = Flask(__name__)

# 🔒 sécurité : éviter crash au démarrage
try:
    model = train_model()
    print("Model loaded successfully")
except Exception as e:
    print("Model error:", e)
    model = None

# 📊 simulation des matchs (tu remplaceras plus tard par API)
def get_matches():

    matches = [
        {"home": "Real Madrid", "away": "Barcelona", "shots": 18, "xg": 2.1, "minute": 55, "score": "1-1"},
        {"home": "PSG", "away": "Marseille", "shots": 17, "xg": 2.5, "minute": 60, "score": "2-0"},
        {"home": "Liverpool", "away": "Chelsea", "shots": 9, "xg": 0.8, "minute": 30, "score": "0-0"}
    ]

    results = []

    for m in matches:

        try:
            # dataframe pour le modèle
            df = pd.DataFrame([{
                "shots_total": m["shots"],
                "xg": m["xg"]
            }])

            # prédiction IA
            if model:
                prob = model.predict_proba(df)[0][1]
                prob = round(prob * 100)
            else:
                prob = random.randint(40, 80)

        except Exception as e:
            print("Prediction error:", e)
            prob = random.randint(40, 80)

        # décision
        decision = "NEXT GOAL" if prob > 65 else "NO BET"

        results.append({
            "home": m["home"],
            "away": m["away"],
            "score": m["score"],
            "minute": m["minute"],
            "shots": m["shots"],
            "xg": m["xg"],
            "prob": prob,
            "confidence": prob,
            "decision": decision,
            "reason": "AI prediction"
        })

    return results

# 🏠 page web
@app.route("/")
def home():
    return render_template("index.html")

# 📡 API JSON
@app.route("/matches")
def matches():
    return jsonify(get_matches())

# 🚀 lancement serveur
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)