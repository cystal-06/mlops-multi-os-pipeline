from pydantic import BaseModel, Field

class SentimentRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="Text to analyze sentiment",
        example="This Linux MLOps system deployed on Arch Linux is incredibly fast and secure!"
    )

class SentimentResponse(BaseModel):
    model_name: str
    model_version: str
    input_text: str
    label: str
    confidence_score: float
    is_positive: bool

class BatchSentimentRequest(BaseModel):
    texts: list[str] = Field(
        ...,
        min_items=1,
        max_items=50,
        description="List of sentences for batch inference",
        example=[
            "Arch Linux rolling release is wonderful and up to date.",
            "Server connection timed out with critical failure."
        ]
    )

class BatchSentimentResponse(BaseModel):
    model_name: str
    total_processed: int
    results: list[SentimentResponse]
