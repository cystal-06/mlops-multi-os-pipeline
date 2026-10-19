import os
import joblib
import numpy as np
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

DEFAULT_MODEL_PATH = "/app/models/rf_model.joblib"

def ensure_model():
    os.makedirs(os.path.dirname(DEFAULT_MODEL_PATH), exist_ok=True)
    if not os.path.exists(DEFAULT_MODEL_PATH):
        X, y = load_iris(return_X_y=True)
        clf = RandomForestClassifier(n_estimators=50, max_depth=4, random_state=42)
        clf.fit(X, y)
        joblib.dump(clf, DEFAULT_MODEL_PATH)
    return joblib.load(DEFAULT_MODEL_PATH)

def load_model(path: str = DEFAULT_MODEL_PATH):
    if os.path.exists(path):
        return joblib.load(path)
    return ensure_model()
