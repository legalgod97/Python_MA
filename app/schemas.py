from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class MediaFileSchema(BaseModel):
  uid: UUID
  original_filename: str
  file_format: str
  file_size: int
  cloud_storage_path: Optional[str] = None


class MediaFileCreateSchema(BaseModel):
  file: bytes
  original_filename: str
  file_format: str
  file_size: int
