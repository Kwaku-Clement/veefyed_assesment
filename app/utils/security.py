from fastapi import Security, HTTPException, status
from fastapi.security import APIKeyHeader
import os

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# In a real scenario, this would be in an environment variable
# For this assessment, we'll default to a simple key if not set
EXPECTED_API_KEY = os.getenv("API_KEY", "secret-token-123")

async def get_api_key(api_key_header: str = Security(api_key_header)):
    if api_key_header == EXPECTED_API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials"
    )
