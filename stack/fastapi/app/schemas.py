from pydantic import BaseModel

class OCRResponse(BaseModel):
    status: str
    model_engine: str
    model_version: str
    filename: str
    image_resolution: str
    extracted_text: str
    word_count: int
    char_count: int
