from fastapi import FastAPI, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator

from app.schemas import (
    TextAnalysisRequest,
    TextAnalysisResponse,
    BatchTextRequest,
    BatchTextResponse,
)
from app.nlp_analyzer import analyze_sentiment

app = FastAPI(
    title="MLOps Production NLP Serving Service",
    description="High-Throughput Text Sentiment & Semantic Scanner on Arch Linux",
    version="2.0.0",
)

Instrumentator().instrument(app).expose(app)

current_model_version = "v2.0.0-nlp-lexicon-engine"
MODEL_NAME = "NLP-Sentiment-Scanner-Core"

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "status": "healthy",
        "service": "mlops-nlp-serving",
        "model_name": MODEL_NAME,
        "model_version": current_model_version,
    }

@app.post("/v1/predict", response_model=TextAnalysisResponse, status_code=status.HTTP_200_OK)
def scan_text(request: TextAnalysisRequest):
    try:
        nlp_res = analyze_sentiment(request.text)
        return TextAnalysisResponse(
            model_name=MODEL_NAME,
            model_version=current_model_version,
            input_text=request.text,
            sentiment_label=nlp_res["label"],
            confidence_score=nlp_res["confidence_score"],
            sentiment_score=nlp_res["sentiment_score"],
            word_count=nlp_res["word_count"],
            matched_sentiment_tokens=nlp_res["highlighted_tokens"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"NLP Scan error: {str(e)}")

@app.post("/v1/predict/batch", response_model=BatchTextResponse, status_code=status.HTTP_200_OK)
def scan_text_batch(batch: BatchTextRequest):
    if not batch.documents:
        raise HTTPException(status_code=400, detail="Document list cannot be empty")

    results = []
    for doc in batch.documents:
        nlp_res = analyze_sentiment(doc)
        results.append(
            TextAnalysisResponse(
                model_name=MODEL_NAME,
                model_version=current_model_version,
                input_text=doc,
                sentiment_label=nlp_res["label"],
                confidence_score=nlp_res["confidence_score"],
                sentiment_score=nlp_res["sentiment_score"],
                word_count=nlp_res["word_count"],
                matched_sentiment_tokens=nlp_res["highlighted_tokens"],
            )
        )

    return BatchTextResponse(
        total_processed=len(results),
        results=results,
    )

@app.post("/v1/models/reload", status_code=status.HTTP_200_OK)
def reload_model(new_version: str = "v2.1.0-hot-reloaded"):
    global current_model_version
    current_model_version = new_version
    return {
        "status": "success",
        "message": "NLP engine reloaded with zero downtime",
        "active_model_version": current_model_version,
    }
