# Image Analysis API

A backend service for mobile apps that handles image uploads and performs mock AI-based skin analysis.

## How to Run the Service

### Option 1: Local Python
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Option 2: Docker
```bash
# Build image
docker build -t image-analysis-api .

# Run container
docker run -p 8000:8000 image-analysis-api
```

The API will be available at `http://localhost:8000`

## Authentication

All endpoints are protected by an API Key authentication. You must include the `X-API-Key` header in your requests.

**Default API Key:** `secret-token-123`

## Available Endpoints

### POST /upload

Upload an image file and receive an image_id.

**Request:**
- Method: POST
- Header: `X-API-Key: secret-token-123`
- Content-Type: multipart/form-data
- Body: file (JPEG or PNG, max 5MB)

**Response:**
```json
{
  "image_id": "abc123"
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/upload \
  -H "X-API-Key: secret-token-123" \
  -F "file=@image.jpg"
```

### POST /analyze

Analyze an uploaded image by its image_id.

**Request:**
- Method: POST
- Header: `X-API-Key: secret-token-123`
- Content-Type: application/json
- Body:
```json
{
  "image_id": "abc123"
}
```

**Response:**
```json
{
  "image_id": "abc123",
  "skin_type": "Oily",
  "issues": ["Hyperpigmentation"],
  "confidence": 0.87
}
```

**Example:**
```bash
curl -X POST http://localhost:8000/analyze \
  -H "X-API-Key: secret-token-123" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "abc123"}'
```

## Assumptions

1. Mock Analysis: The analyze endpoint returns randomized mock results (skin type, issues, confidence). No actual AI model is implemented.
2. Local Storage: Images are stored in the `uploads/` directory on the local file system.
3. In-Memory Metadata: Image metadata is stored in memory and will be lost when the server restarts.
4. Single Instance: Designed for single-instance deployment without distributed storage.

## Improvements for Production

If this were a production-grade application, I would implement the following improvements:

1. **Persistent Storage**: Replace local file storage with cloud object storage (e.g., AWS S3, Google Cloud Storage) for scalability and reliability.
2. **Database Integration**: Use a proper database (PostgreSQL/MongoDB) instead of in-memory dictionaries to persist image metadata and analysis results.
3. **Authentication & Authorization**: Implement robust authentication (OAuth2/JWT) to secure endpoints and manage user access.
4. **Asynchronous Processing**: Offload heavy AI analysis tasks to a background worker queue (e.g., Celery, Redis) to prevent blocking the main application thread.
5. **Real AI Integration**: Integrate actual Machine Learning models (PyTorch/TensorFlow) for skin analysis instead of mock logic.
6. **Input Validation**: Add more rigorous validation for image formats (magic numbers) and sanitization to prevent security vulnerabilities.
7. **CI/CD Pipeline**: Set up automated testing and deployment pipelines.
8. **Monitoring & Alerting**: Implement tools like Prometheus/Grafana or Sentry for real-time monitoring and error tracking.

## Project Structure
skin-analysis-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── analysis.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── image_service.py
│   └── utils/
│       ├── __init__.py
│       └── validators.py
├── uploads/
│   └── .gitkeep
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md

## Setup Commands

# Create folder structure
mkdir -p app/routes app/services app/utils uploads

# Create all files (copy content from above)
# Then run:
pip install -r requirements.txt
uvicorn app.main:app --reload