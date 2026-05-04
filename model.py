import pandas as pd
from sklearn.linear_model import LogisticRegression

def train_model():
    try:
        df = pd.read_csv("dataset.csv")

        X = df[["shots_total", "xg"]]
        y = df["goal"]

        model = LogisticRegression()
        model.fit(X, y)

        return model

    except Exception as e:
        print("ERREUR MODEL:", e)

        # modèle fallback (évite crash)
        class DummyModel:
            def predict_proba(self, X):
                return [[0.3, 0.7] for _ in range(len(X))]

        return DummyModel()