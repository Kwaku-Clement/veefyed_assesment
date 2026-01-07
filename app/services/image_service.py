import uuid
import random
from pathlib import Path
from fastapi import UploadFile
from app.utils.validators import validate_file
import logging

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# In-memory store for image metadata
image_store = {}


async def save_image(file: UploadFile) -> str:
    """Save uploaded image and return image_id"""
    content = await file.read()
    
    # Validate file
    validate_file(file.filename, content)
    
    # Generate image_id
    image_id = str(uuid.uuid4())[:8]
    
    # Get file extension
    file_ext = Path(file.filename).suffix.lower()
    
    # Save file
    file_path = UPLOAD_DIR / f"{image_id}{file_ext}"
    with open(file_path, "wb") as f:
        f.write(content)
    
    logger.info(f"Saved image to {file_path}")
    
    # Store metadata
    image_store[image_id] = {
        "filename": file.filename,
        "path": str(file_path)
    }
    
    return image_id


def analyze_image(image_id: str) -> dict:
    """Perform mock analysis on image"""
    if image_id not in image_store:
        raise FileNotFoundError(f"Image with id '{image_id}' not found")
    
    logger.info(f"Running mock analysis for {image_id}")
    
    # Mock AI analysis
    skin_types = ["Oily", "Dry", "Combination", "Normal", "Sensitive"]
    issues = ["Hyperpigmentation", "Acne", "Fine Lines", "Dark Spots", "Redness", "Uneven Texture"]
    
    result = {
        "image_id": image_id,
        "skin_type": random.choice(skin_types),
        "issues": random.sample(issues, random.randint(1, 3)),
        "confidence": round(random.uniform(0.75, 0.95), 2)
    }
    
    logger.info(f"Analysis result: {result['skin_type']}, confidence: {result['confidence']}")
    
    return result