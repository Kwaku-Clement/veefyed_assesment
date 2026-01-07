from fastapi import FastAPI
from app.routes import analysis
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI()

app.include_router(analysis.router)


@app.get("/")
def root():
    return {
        "service": "Image Analysis API",
        "status": "running"
    }