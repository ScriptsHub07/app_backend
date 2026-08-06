from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.types import JSON
from datetime import datetime
from .db import Base


class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class OAuthToken(Base):
    __tablename__ = "oauth_tokens"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(255), index=True)
    provider = Column(String(50), index=True)
    token = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
