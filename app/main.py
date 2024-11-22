import uvicorn
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException, BackgroundTasks, Response, status
from app.schemas import MediaFileSchema, MediaFileCreateSchema
from app.database import get_db
from app.crud import create_media_file, get_media_file_by_uid
from app.utils import generate_uid, save_file
from app.tasks import upload_media_to_cloud
from fastapi.responses import StreamingResponse
import os
from typing import Optional
from uuid import UUID

app = FastAPI()

@app.post("/media", response_model=MediaFileSchema, status_code=status.HTTP_201_CREATED)
async def upload_media(file: UploadFile = File(...), background_tasks: BackgroundTasks = BackgroundTasks(), db: Session = Depends(get_db)):
  file_content = await file.read()
  uid = generate_uid()
  file_extension = os.path.splitext(file.filename)[1]
  file_path = save_file(file_content, f"{uid}{file_extension}", os.getenv("MEDIA_STORAGE_PATH"))
  media_file = MediaFile(original_filename=file.filename, file_format=file_extension[1:], file_size=len(file_content))
  media_file = create_media_file(db, media_file)
  background_tasks.add_task(upload_media_to_cloud, file_path, str(media_file.uid), db)
  return {"uid": media_file.uid, "original_filename": file.filename, "file_format": file_extension[1:], "file_size": len(file_content)}


@app.get("/media/{uid}", response_class=StreamingResponse)
async def get_media(uid: UUID, db: Session = Depends(get_db)):
 media_file = get_media_file_by_uid(db, str(uid))
 if not media_file:
  raise HTTPException(status_code=404, detail="File not found")
 file_path = os.path.join(os.getenv("MEDIA_STORAGE_PATH"), str(media_file.uid) + media_file.file_format)
 async with aiofiles.open(file_path, mode='rb') as f:
   async def file_generator():
     while True:
       chunk = await f.read(1024 * 1024) # 1 MB chunks
       if not chunk:
         break
       yield chunk
   return StreamingResponse(file_generator(), media_type="application/octet-stream")



if __name__ == "__main__":
  uvicorn.run(app, host="0.0.0.0", port=8000)