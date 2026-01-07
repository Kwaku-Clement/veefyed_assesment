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

This service is designed with scalability and maintainability in mind. While currently a "small backend service" suitable for an MVP, it includes several architectural decisions that pave the way for a full production deployment.

### Current Production-Ready Features
*   Security First: Implemented API Key authentication (`X-API-Key`) to protect all endpoints from unauthorized access.
*   Robust Input Validation: Beyond simple file extension checks, the service validates file "magic numbers" (binary signatures) to prevent malicious uploads (e.g., renaming an executable to `.jpg`).
*   Observability: Custom middleware logs every request duration and status code, providing essential visibility into API performance and usage patterns.
*   Standardized Error Handling: Consistent HTTP error responses (400, 403, 404) with clear, actionable messages for client consumers.
*   Containerization: A production-ready `Dockerfile` ensures consistent execution environments, from local development to cloud clusters.

### Roadmap to Full Scale
To scale this service for high-volume production traffic, the following enhancements are recommended:

1.  **Data Persistence:**
    *   Database: Migrate from in-memory `image_store` to a persistent SQL (PostgreSQL) or NoSQL (MongoDB) database to track analysis history and user metadata.
    *   Object Storage: Offload image storage from the local filesystem to a cloud object store (AWS S3, Google Cloud Storage, or Azure Blob Storage) for infinite scalability and better durability.

2.  **Performance & Security:**
    *   Rate Limiting: Implement rate limiting (e.g., using Redis) to prevent abuse and ensure fair resource usage.
    *   Asynchronous Processing: Move the image analysis (which can be CPU-intensive) to a background task queue (e.g., Celery + Redis) to keep the API responsive under load.
    *   HTTPS: Enforce SSL/TLS for all communication.

3.  **DevOps & Testing:**
    *   CI/CD: Automated pipelines for testing, linting, and deployment.
    *   Testing: Expand the current test scripts into a full suite of unit and integration tests using `pytest`.
    *   Monitoring: Integrate with tools like Prometheus/Grafana or Datadog for real-time alerts and deeper metrics.

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