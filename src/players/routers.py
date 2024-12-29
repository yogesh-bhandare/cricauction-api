from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import PlayerResponseModel, PlayerRequestModel
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import Player
from typing import List, Optional


router = APIRouter(
    prefix="/players",
    tags=['Players']
)

# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PlayerResponseModel)
def add_player(request:PlayerRequestModel, db:Session=Depends(get_db)):
    new_player = Player(**request.model_dump())
    if not new_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not added!")
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# Read
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[PlayerResponseModel])
def get_players(db:Session=Depends(get_db), search:str="", limit:int=10, skip=0):
    players = db.query(Player).filter(Player.first_name.contains(search)).limit(limit).offset(skip).all()
    if not players:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Players not added!")
    return players

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=PlayerResponseModel)
def get_player_by_id(id:int, db:Session=Depends(get_db)):
    player = db.query(Player).filter(Player.id == id).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    return player

# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=PlayerResponseModel) 
def update_player(id:int, request:PlayerRequestModel, db:Session=Depends(get_db)):
    player = db.query(Player).filter(Player.id == id)
    if not player.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    player.update(request.model_dump(), synchronize_session=False)
    db.commit()
    update_player = player.first()
    return update_player

# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_player(id:int, db:Session=Depends(get_db)):
    player = db.query(Player).filter(Player.id == id)
    if not player.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    player.delete(synchronize_session=False)
    return {"response":"Player deleted successfully!"}
    