import asyncio
from app.cloud_storage import upload_to_cloud
from app.crud import create_media_file
from app.models import MediaFile
from app.schemas import MediaFileSchema
from sqlalchemy.orm import Session
from fastapi import Depends, BackgroundTasks

async def upload_media_to_cloud(file_path: str, uid: str, db: Session, background_tasks: BackgroundTasks):
 cloud_path = await upload_to_cloud(file_path, uid)
 media_file = get_media_file_by_uid(db, uid)
 media_file.cloud_storage_path = cloud_path
 db.commit()