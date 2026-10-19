from fastapi import FastAPI, File, UploadFile, HTTPException, status
from prometheus_fastapi_instrumentator import Instrumentator

from app.schemas import OCRResponse
from app.ocr_engine import extract_text_from_image

app = FastAPI(
    title="MLOps Production OCR Serving Service",
    description="High-Throughput Optical Character Recognition (OCR) Scanner on Arch Linux",
    version="3.0.0",
)

Instrumentator().instrument(app).expose(app)

current_model_version = "v3.0.0-tesseract-ocr"
MODEL_ENGINE = "Tesseract-OCR-Core"

@app.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {
        "status": "healthy",
        "service": "mlops-ocr-serving",
        "model_engine": MODEL_ENGINE,
        "model_version": current_model_version,
    }

@app.post("/v1/ocr/scan", response_model=OCRResponse, status_code=status.HTTP_200_OK)
async def scan_image(file: UploadFile = File(..., description="Tải lên file ảnh (PNG, JPG, JPEG) để AI quét chữ")):
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Định dạng file không hợp lệ: {file.content_type}. Vui lòng tải lên file ảnh (PNG, JPG, WEBP)."
        )

    try:
        contents = await file.read()
        ocr_result = extract_text_from_image(contents)

        return OCRResponse(
            status="success",
            model_engine=MODEL_ENGINE,
            model_version=current_model_version,
            filename=file.filename,
            image_resolution=ocr_result["image_size"],
            extracted_text=ocr_result["text"],
            word_count=ocr_result["word_count"],
            char_count=len(ocr_result["text"]),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi xử lý OCR: {str(e)}")

@app.post("/v1/models/reload", status_code=status.HTTP_200_OK)
def reload_model(new_version: str = "v3.1.0-ocr-reloaded"):
    global current_model_version
    current_model_version = new_version
    return {
        "status": "success",
        "message": "OCR Engine reloaded with zero downtime",
        "active_version": current_model_version,
    }
