# routers/rooms.py
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_user

router = APIRouter(prefix="/rooms", tags=["房间系统"])

@router.post("/create", response_model=schemas.RoomBase)
def create_room(db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    room = models.Room(owner_id=user.id)
    db.add(room)
    db.commit()
    db.refresh(room)
    return room

@router.get("/", response_model=List[schemas.RoomBase])
def list_rooms(db: Session = Depends(database.get_db)):
    return db.query(models.Room).filter(models.Room.is_started == False).all()

@router.post("/{room_id}/join", response_model=schemas.RoomBase)
def join_room(room_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(404, "房间不存在")
    if room.player2_id:
        raise HTTPException(400, "房间已满")
    if room.owner_id == user.id:
        raise HTTPException(400, "你已在房间中")
    room.player2_id = user.id
    room.is_started = True
    db.commit()
    db.refresh(room)
    return room

@router.post("/{room_id}/leave")
def leave_room(room_id: int, db: Session = Depends(database.get_db), user=Depends(get_current_user)):
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(404, "房间不存在")
    if room.owner_id == user.id or room.player2_id == user.id:
        db.delete(room)
        db.commit()
        return {"msg": "你已离开房间，房间已解散"}
    else:
        raise HTTPException(403, "你不在房间中")
