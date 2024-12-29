from fastapi import APIRouter, Depends, HTTPException, status
from ..db.models import Auction, Team, Player, Summary
from ..db.connect import get_db
from sqlalchemy.orm import Session
from .schemas import TeamSummaryResponse, PlayerSoldRequest
from typing import List

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

# Adds sold player details to Summary model for transaction history and also updates both Teams and Players models
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TeamSummaryResponse)
def player_sold_team(request:PlayerSoldRequest, db:Session=Depends(get_db)):
    player = db.query(Player).filter(Player.id == request.player_id).first()
    team = db.query(Team).filter(Team.id == request.team_id).first()
    new_bid = Summary(**request.model_dump())

    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
    if not new_bid:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not added successfully!")

    db.add(new_bid)
    player.is_sold = True
    player.sold_price = request.sold_price
    player.team_id = request.team_id
    team.remaining_purse -= request.sold_price
    db.commit()
    db.refresh(new_bid)
    return new_bid

# Summay 
@router.get('/', status_code=status.HTTP_200_OK)
def get_summary(db:Session=Depends(get_db)):
    summary = db.query(Summary).all()
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found!")
    return summary


# Teams Summary to see which player they bought
@router.get('/team/{id}', status_code=status.HTTP_200_OK, response_model=List[TeamSummaryResponse])
def team_summary(id:int, db:Session=Depends(get_db)):
    sold_players_list = db.query(Summary).filter(Summary.team_id == id).all()
    if not sold_players_list:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team Not Found")
    return sold_players_list
