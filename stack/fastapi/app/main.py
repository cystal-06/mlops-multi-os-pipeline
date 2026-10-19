from fastapi import FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator

from app.schemas import (
    SentimentRequest,
    SentimentResponse,
    BatchSentimentRequest,
    BatchSentimentResponse,
)
from app.model_manager import get_sentiment_model, reload_sentiment_model

app = FastAPI(
    title="MLOps Production NLP Serving Service",
    description="High-Throughput Sentiment Analysis Inference Microservice with Prometheus Telemetry",
    version="2.0.0",
)

Instrumentator().instrument(app).expose(app)

current_model_version = "v1.0.0-distilbert"
current_model_name = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "status": "healthy",
        "service": "mlops-sentiment-inference",
        "model_name": current_model_name,
        "model_version": current_model_version,
    }

@app.post("/v1/predict", response_model=SentimentResponse, status_code=status.HTTP_200_OK)
def predict(request: SentimentRequest):
    try:
        classifier = get_sentiment_model(current_model_name)
        result = classifier(request.text)[0]
        label = result["label"].upper()
        score = round(float(result["score"]), 4)

        return SentimentResponse(
            model_name=current_model_name,
            model_version=current_model_version,
            input_text=request.text,
            label=label,
            confidence_score=score,
            is_positive=(label == "POSITIVE"),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference error: {str(e)}")

@app.post("/v1/predict/batch", response_model=BatchSentimentResponse, status_code=status.HTTP_200_OK)
def predict_batch(batch_request: BatchSentimentRequest):
    if not batch_request.texts:
        raise HTTPException(status_code=400, detail="Texts list cannot be empty")

    try:
        classifier = get_sentiment_model(current_model_name)
        raw_results = classifier(batch_request.texts)

        formatted = []
        for text, res in zip(batch_request.texts, raw_results):
            label = res["label"].upper()
            score = round(float(res["score"]), 4)
            formatted.append(
                SentimentResponse(
                    model_name=current_model_name,
                    model_version=current_model_version,
                    input_text=text,
                    label=label,
                    confidence_score=score,
                    is_positive=(label == "POSITIVE"),
                )
            )

        return BatchSentimentResponse(
            model_name=current_model_name,
            total_processed=len(formatted),
            results=formatted,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch inference error: {str(e)}")

@app.post("/v1/models/reload", status_code=status.HTTP_200_OK)
def reload_model(new_version: str = "v2.0.0-distilbert-reloaded"):
    global current_model_version
    reload_sentiment_model(current_model_name)
    current_model_version = new_version
    return {
        "status": "success",
        "message": "Hugging Face model reloaded in RAM with zero downtime",
        "active_version": current_model_version,
    }
