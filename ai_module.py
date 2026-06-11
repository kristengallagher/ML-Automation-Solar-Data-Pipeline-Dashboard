from sklearn.ensemble import IsolationForest

def train_model(X):
    model = IsolationForest(
        n_estimators=100,
        max_samples='auto',
        contamination=0.01,
        random_state=42
    )
    model.fit(X)
    return model

def predict(model, X):
    return model.predict(X)
