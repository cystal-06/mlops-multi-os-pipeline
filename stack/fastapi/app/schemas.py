from pydantic import BaseModel, Field

class FeaturesInput(BaseModel):
    sepal_length: float = Field(..., ge=0.1, le=10.0, example=5.1)
    sepal_width: float = Field(..., ge=0.1, le=10.0, example=3.5)
    petal_length: float = Field(..., ge=0.1, le=10.0, example=1.4)
    petal_width: float = Field(..., ge=0.1, le=10.0, example=0.2)

class PredictionResponse(BaseModel):
    model_name: str
    model_version: str
    predicted_class: int
    predicted_label: str
    confidence_score: float

class BatchFeaturesInput(BaseModel):
    instances: list[FeaturesInput]

class BatchPredictionResponse(BaseModel):
    model_name: str
    total_predictions: int
    predictions: list[PredictionResponse]
