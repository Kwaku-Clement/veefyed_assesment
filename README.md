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

## Documentation

Interactive documentation is available at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## Authentication

All endpoints are protected by an API Key authentication. You must include the `X-API-Key` header in your requests.

**Default API Key:** `secret-token-123`

## Available Endpoints

### POST /upload

Upload an image file and receive an image_id.

Request:
- Method: POST
- Header: `X-API-Key: secret-token-123`
- Content-Type: multipart/form-data
- Body: file (JPEG or PNG, max 5MB)

Response:
```json
{
  "image_id": "abc123"
}
```

Example:
```bash
curl -X POST http://localhost:8000/upload \
  -H "X-API-Key: secret-token-123" \
  -F "file=@image.jpg"
```

### POST /analyze

Analyze an uploaded image by its image_id.

Request:
- Method: POST
- Header: `X-API-Key: secret-token-123`
- Content-Type: application/json
- Body:
```json
{
  "image_id": "abc123"
}
```

Response:
```json
{
  "image_id": "abc123",
  "skin_type": "Oily",
  "issues": ["Hyperpigmentation"],
  "confidence": 0.87
}
```

Example:
```bash
curl -X POST http://localhost:8000/analyze \
  -H "X-API-Key: secret-token-123" \
  -H "Content-Type: application/json" \
  -d '{"image_id": "abc123"}'
```

## Assumptions
- For the purpose of this assessment, the `image_store` is in-memory. In a production environment, this would be replaced with a database (e.g., PostgreSQL or MongoDB).
- The `secret-token-123` is a default API key for demonstration. In production, this would be managed via environment variables or a secure vault.
- Image storage is local. For production, a cloud-based storage like AWS S3 or Google Cloud Storage would be preferred.

## Production Readiness & Improvements
While this service is designed to be a "small backend service" as per the requirements, it includes several features that move it closer to production readiness:
1.  Security: Implemented API Key authentication to protect endpoints.
2.  Validation: Added deep file validation using magic numbers (binary signatures) to prevent malicious file uploads that bypass extension checks.
3.  Logging: Structured logging with request/response middleware for full auditability and performance monitoring.
4.  Containerization: Provided a `Dockerfile` for consistent deployment across environments.
5.  Interactive Documentation: Custom ReDoc and SwaggerUI integration for easier integration testing.

For a full production rollout, further improvements would include:
- Persistent storage (Database and Cloud Storage).
- Comprehensive unit and integration test suite (built on the provided test scripts).
- Rate limiting to prevent abuse.
- CI/CD pipeline integration.

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