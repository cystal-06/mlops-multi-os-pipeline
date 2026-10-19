import os
from transformers import pipeline

DEFAULT_MODEL_NAME = "distilbert/distilbert-base-uncased-finetuned-sst-2-english"
_cached_pipeline = None

def get_sentiment_model(model_name: str = DEFAULT_MODEL_NAME):
    global _cached_pipeline
    if _cached_pipeline is None:
        _cached_pipeline = pipeline(
            "sentiment-analysis",
            model=model_name,
            device=-1
        )
    return _cached_pipeline

def reload_sentiment_model(new_model_name: str = DEFAULT_MODEL_NAME):
    global _cached_pipeline
    _cached_pipeline = pipeline(
        "sentiment-analysis",
        model=new_model_name,
        device=-1
    )
    return _cached_pipeline
