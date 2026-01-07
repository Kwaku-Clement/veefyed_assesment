from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def validate_file(filename: str, content: bytes):
    """Validate file type and size"""
    # Check file type
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Check file size
    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File too large. Max size: 5MB")