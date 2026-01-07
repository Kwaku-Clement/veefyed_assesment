from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Magic numbers (signatures) for file types
MAGIC_NUMBERS = {
    "jpg": b"\xFF\xD8\xFF",
    "jpeg": b"\xFF\xD8\xFF",
    "png": b"\x89PNG\r\n\x1a\n"
}

def validate_file(filename: str, content: bytes):
    """Validate file type, size, and magic numbers"""
    # Check file size first (fail fast)
    if len(content) > MAX_FILE_SIZE:
        raise ValueError("File too large. Max size: 5MB")

    # Check file extension
    file_ext = Path(filename).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}")
    
    # Check magic numbers
    ext_key = file_ext.lstrip(".")
    # Handle jpg/jpeg alias
    if ext_key == "jpg":
        expected_magic = MAGIC_NUMBERS["jpeg"]
    elif ext_key == "jpeg":
        expected_magic = MAGIC_NUMBERS["jpeg"]
    else:
        expected_magic = MAGIC_NUMBERS.get(ext_key)

    if expected_magic and not content.startswith(expected_magic):
         raise ValueError(f"Invalid file content. The file claims to be {file_ext} but the content does not match.")