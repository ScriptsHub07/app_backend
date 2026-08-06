from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

from ..db import SessionLocal, init_db
from .. import models

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class MemoryItem(BaseModel):
    id: int = None
    title: str
    text: str


@router.post("/", response_model=MemoryItem)
def create_memory(item: MemoryItem, db: Session = Depends(get_db)):
    m = models.Memory(title=item.title, text=item.text)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m


@router.get("/", response_model=List[MemoryItem])
def list_memory(db: Session = Depends(get_db)):
    return db.query(models.Memory).order_by(models.Memory.created_at.desc()).all()


@router.get("/{item_id}", response_model=MemoryItem)
def get_memory(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Memory).filter(models.Memory.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Not found")
    return item
