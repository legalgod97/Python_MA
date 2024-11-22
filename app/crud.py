import os
from sqlalchemy.orm import Session
from app.models import MediaFile
from app.schemas import MediaFileSchema, MediaFileCreateSchema


def create_media_file(db: Session, media_file: MediaFile):
  db.add(media_file)
  db.commit()
  db.refresh(media_file)
  return media_file

def get_media_file_by_uid(db: Session, uid: str):
  return db.query(MediaFile).filter(MediaFile.uid == uid).first()