from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import PlayerResponseModel, PlayerRequestModel
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import Player, Auction
from typing import List
from ..auth.utils import require_role
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData


router = APIRouter(
    prefix="/players",
    tags=['Players']
)

# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=PlayerResponseModel, dependencies=[Depends(require_role(["admin", "user"]))])
def add_player(request:PlayerRequestModel, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id, Auction.id == request.auction_id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access")
    new_player = Player(**request.model_dump())
    if not new_player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not added!")
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player

# Read
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=List[PlayerResponseModel], dependencies=[Depends(require_role(["admin", "user"]))])
def get_players(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user), search:str="", limit:int=10, skip=0):
    auction = db.query(Auction).filter(Auction.user_id == user.id, Auction.id == id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    players = db.query(Player).filter(Player.auction_id == id, Player.first_name.contains(search)).limit(limit).offset(skip).all()
    if not players:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Players not added!")
    return players

@router.get('/by/{id}', status_code=status.HTTP_200_OK, response_model=PlayerResponseModel, dependencies=[Depends(require_role(["admin", "user"]))])
def get_player_by_id(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    player = db.query(Player).filter(Player.id == id).first()
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    return player

# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=PlayerResponseModel, dependencies=[Depends(require_role(["admin", "user"]))]) 
def update_player(id:int, request:PlayerRequestModel, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    player = db.query(Player).filter(Player.id == id)
    if not player.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    player.update(request.model_dump(), synchronize_session=False)
    db.commit()
    update_player = player.first()
    return update_player

# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["admin", "user"]))])
def delete_player(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    player = db.query(Player).filter(Player.id == id)
    if not player.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    player.delete(synchronize_session=False)
    return {"response":"Player deleted successfully!"}
    