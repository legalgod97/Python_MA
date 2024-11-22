import uuid
from sqlalchemy import create_engine, Column, String, Integer, LargeBinary, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class MediaFile(Base):
    __tablename__ = "media_files"
    uid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_filename = Column(Text, nullable=False)
    file_format = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    data = Column(LargeBinary) # Не храним данные здесь, только ссылка
    cloud_storage_path = Column(Text) #Ссылка на облачное хранилище

    def __repr__(self):
        return f"<MediaFile(uid={self.uid}, filename='{self.original_filename}')>"

engine = create_engine('postgresql://user:password@db:5432/media_db')
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)