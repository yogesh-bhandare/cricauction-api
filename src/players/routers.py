from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import PlayerResponse, PlayerRequest
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import Player
from typing import List
from ..auth.utils import require_role, verify_auction_access
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData


router = APIRouter(
    prefix="/players",
    tags=['Players']
)


# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PlayerResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def add_player(request:PlayerRequest, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        verify_auction_access(db, current_user.id, request.auction_id)
        new_player = Player(**request.model_dump())
        if not new_player:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Player not added!")
        db.add(new_player)
        db.commit()
        db.refresh(new_player)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return new_player


# Read
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=List[PlayerResponse], dependencies=[Depends(require_role(["admin", "user"]))])
def get_players(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user), search:str="", limit:int=10, skip=0):
    try:
        verify_auction_access(db, current_user.id, id)
        players = db.query(Player).filter(Player.auction_id == id, Player.first_name.contains(search)).limit(limit).offset(skip).all()
        if not players:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Players not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return players


@router.get('/by/{id}', status_code=status.HTTP_200_OK, response_model=PlayerResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def get_player_by_id(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        player = db.query(Player).filter(Player.id == id).first()
        if not player:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    verify_auction_access(db, current_user.id, player.auction_id)
    return player


# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=PlayerResponse, dependencies=[Depends(require_role(["admin", "user"]))]) 
def update_player(id:int, request:PlayerRequest, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        player = db.query(Player).filter(Player.id == id)
        if not player.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
        verify_auction_access(db, current_user.id, player.first().auction_id)
        player.update(request.model_dump(), synchronize_session=False)
        db.commit()
        update_player = player.first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return update_player


# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["admin", "user"]))])
def delete_player(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        player = db.query(Player).filter(Player.id == id)
        if not player.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
        verify_auction_access(db, current_user.id, player.first().auction_id)
        player.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return {"response":"Player deleted successfully!"}
    