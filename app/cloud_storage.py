import asyncio
import os
from app.schemas import MediaFileSchema

async def upload_to_cloud(file_path: str, uid: str) -> str:
  """Имитация загрузки в облако"""
  await asyncio.sleep(1) # Имитация задержки
  cloud_path = f"/cloud/{uid}" #Имитация пути в облаке
  return cloud_path