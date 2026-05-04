import pandas as pd
from xgboost import XGBClassifier

data = pd.DataFrame([
    [2.1, 10, 55, 1],
    [2.5, 12, 60, 1],
    [0.8, 5, 30, 0],
    [1.2, 7, 40, 0],
    [3.0, 15, 70, 1],
    [0.5, 3, 20, 0]
], columns=["xg", "shots", "minute", "goal"])

X = data[["xg", "shots", "minute"]]
y = data["goal"]

model = XGBClassifier()
model.fit(X, y)

def predict_goal(xg, shots, minute):
    prob = model.predict_proba([[xg, shots, minute]])[0][1]
    return round(prob * 100, 2)