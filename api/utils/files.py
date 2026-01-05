import os
from pathlib import Path
import uuid

from fastapi import HTTPException, UploadFile

UPLOAD_DIR = "uploads/"


def sanitize_name(filename: str) -> str:
    return Path(filename).name


async def save_file(file: UploadFile) -> str:
    if file.filename is None:
        raise HTTPException(status_code=400, detail="No file uploaded")

    filename = sanitize_name(file.filename)
    unique_filename = f"{uuid.uuid4()}_{filename}"

    file_path = os.path.join(UPLOAD_DIR, unique_filename)

    try:
        with open(file_path, "wb") as f:
            f.write(await file.read())
            return unique_filename
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error saving file")
