import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="MLOps Model Serving Service")

Instrumentator().instrument(app).expose(app)

current_model_version = "v1-baseline"

class PredictionRequest(BaseModel):
    features: list[float]

class PredictionResponse(BaseModel):
    model_version: str
    prediction: float

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_version": current_model_version
    }

@app.post("/v1/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    if not request.features:
        raise HTTPException(status_code=400, detail="Features list cannot be empty")
    prediction_result = sum(request.features) / len(request.features)
    return PredictionResponse(
        model_version=current_model_version,
        prediction=prediction_result
    )

@app.post("/v1/models/reload")
def reload_model():
    global current_model_version
    current_model_version = "v2-hot-reloaded"
    return {
        "status": "reloaded",
        "new_version": current_model_version
    }
