from sqlalchemy import Column, Integer, String, DateTime
from pgvector.sqlalchemy import Vector
from src.core.database import Base
from datetime import datetime

class NewsDocument(Base):
    __tablename__ = "news_documents"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    embedding = Column(Vector(1536))  # Vector column for 1536-dimensional embeddings
    created_at = Column(DateTime, default=datetime.utcnow)