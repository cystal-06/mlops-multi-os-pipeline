import numpy as np
from fastapi import FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator

from app.schemas import (
    FeaturesInput,
    PredictionResponse,
    BatchFeaturesInput,
    BatchPredictionResponse,
)
from app.model_manager import load_model

app = FastAPI(
    title="MLOps Production Serving Service",
    description="High-Throughput Lightweight Model Serving API on Arch Linux",
    version="1.0.0",
)

Instrumentator().instrument(app).expose(app)

CLASS_NAMES = {0: "setosa", 1: "versicolor", 2: "virginica"}

current_model = load_model()
current_model_version = "v1.0.0-rf-iris"

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "status": "healthy",
        "service": "mlops-serving",
        "model_version": current_model_version,
    }

@app.post("/v1/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
def predict(data: FeaturesInput):
    try:
        sample = np.array([[data.sepal_length, data.sepal_width, data.petal_length, data.petal_width]])
        pred_class = int(current_model.predict(sample)[0])
        probabilities = current_model.predict_proba(sample)[0]
        confidence = float(np.max(probabilities))

        return PredictionResponse(
            model_name="RandomForestClassifier",
            model_version=current_model_version,
            predicted_class=pred_class,
            predicted_label=CLASS_NAMES.get(pred_class, "unknown"),
            confidence_score=round(confidence, 4),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/predict/batch", response_model=BatchPredictionResponse, status_code=status.HTTP_200_OK)
def predict_batch(batch: BatchFeaturesInput):
    if not batch.instances:
        raise HTTPException(status_code=400, detail="Empty instances list")

    results = []
    for item in batch.instances:
        sample = np.array([[item.sepal_length, item.sepal_width, item.petal_length, item.petal_width]])
        pred_class = int(current_model.predict(sample)[0])
        probabilities = current_model.predict_proba(sample)[0]
        confidence = float(np.max(probabilities))
        results.append(
            PredictionResponse(
                model_name="RandomForestClassifier",
                model_version=current_model_version,
                predicted_class=pred_class,
                predicted_label=CLASS_NAMES.get(pred_class, "unknown"),
                confidence_score=round(confidence, 4),
            )
        )

    return BatchPredictionResponse(
        model_name="RandomForestClassifier",
        total_predictions=len(results),
        predictions=results,
    )

@app.post("/v1/models/reload", status_code=status.HTTP_200_OK)
def reload_model():
    global current_model, current_model_version
    current_model = load_model()
    current_model_version = "v1.1.0-reloaded"
    return {
        "status": "success",
        "active_model_version": current_model_version,
    }
