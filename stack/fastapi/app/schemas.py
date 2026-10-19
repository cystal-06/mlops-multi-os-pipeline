from pydantic import BaseModel, Field

class TextAnalysisRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Đoạn văn bản tiếng Anh cần quét và phân tích cảm xúc (NLP)",
        example="This Linux MLOps system on Arch Linux is incredibly fast, clean and very secure!"
    )

class TextAnalysisResponse(BaseModel):
    model_name: str
    model_version: str
    input_text: str
    sentiment_label: str
    confidence_score: float
    sentiment_score: float
    word_count: int
    matched_sentiment_tokens: list[str]

class BatchTextRequest(BaseModel):
    documents: list[str] = Field(
        ...,
        example=[
            "Arch Linux rolling release is awesome, beautiful and super fast!",
            "The database server crashed with critical error and high latency."
        ]
    )

class BatchTextResponse(BaseModel):
    total_processed: int
    results: list[TextAnalysisResponse]
