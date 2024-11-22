import os
import uuid
from pathlib import Path

def generate_uid():
  return str(uuid.uuid4())

def save_file(file_content: bytes, file_name: str, storage_path: str):
  file_path = os.path.join(storage_path, file_name)
  with open(file_path, "wb") as f:
    f.write(file_content)
  return file_path