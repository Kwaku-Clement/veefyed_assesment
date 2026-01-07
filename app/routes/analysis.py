from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from pydantic import BaseModel
from app.services.image_service import save_image, analyze_image as analyze_image_service
from app.utils.security import get_api_key
import logging

logger = logging.getLogger(__name__)

router = APIRouter(dependencies=[Depends(get_api_key)])


class AnalyzeRequest(BaseModel):
    image_id: str


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    logger.info(f"Upload request received: {file.filename}")
    try:
        image_id = await save_image(file)
        logger.info(f"Image uploaded successfully: {image_id}")
        return {"image_id": image_id}
    except ValueError as e:
        logger.warning(f"Upload failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/analyze")
async def analyze(request: AnalyzeRequest):
    logger.info(f"Analyze request for image_id: {request.image_id}")
    try:
        result = analyze_image_service(request.image_id)
        logger.info(f"Analysis complete for {request.image_id}")
        return result
    except FileNotFoundError as e:
        logger.warning(f"Image not found: {request.image_id}")
        raise HTTPException(status_code=404, detail=str(e))
    except ValueError as e:
        logger.warning(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))