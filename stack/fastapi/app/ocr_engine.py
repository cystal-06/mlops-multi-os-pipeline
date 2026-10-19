import io
from PIL import Image
import pytesseract

def extract_text_from_image(image_bytes: bytes) -> dict:
    image = Image.open(io.BytesIO(image_bytes))
    
    # Perform OCR
    extracted_text = pytesseract.image_to_string(image, lang="eng").strip()
    
    # Calculate word count and clean up
    words = extracted_text.split()
    
    return {
        "text": extracted_text if extracted_text else "[NO_TEXT_DETECTED]",
        "word_count": len(words),
        "image_size": f"{image.width}x{image.height}",
        "image_format": image.format if image.format else "UNKNOWN"
    }
