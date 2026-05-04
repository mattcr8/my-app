import pandas as pd
import numpy as np
from xgboost import XGBClassifier

rows = []

for i in range(5000):
    xg = np.random.uniform(0.2, 3.5)
    shots = np.random.randint(1, 20)
    minute = np.random.randint(1, 90)

    prob = (xg * 0.4 + shots * 0.03 + minute * 0.01)
    goal = 1 if prob > 1.5 else 0

    rows.append([xg, shots, minute, goal])

data = pd.DataFrame(rows, columns=["xg","shots","minute","goal"])

X = data[["xg","shots","minute"]]
y = data["goal"]

model = XGBClassifier()
model.fit(X, y)

def predict_goal(xg, shots, minute):
    prob = model.predict_proba([[xg, shots, minute]])[0][1]
    return round(prob * 100, 2)