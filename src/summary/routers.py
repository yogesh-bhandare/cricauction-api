from fastapi import APIRouter, Depends, HTTPException, status
from ..db.models import Auction, Team, Player, Summary
from ..db.connect import get_db
from sqlalchemy.orm import Session
from .schemas import TeamSummaryResponse, PlayerSoldRequest, TeamPlayerSummary
from typing import List
from ..auth.utils import require_role
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData

router = APIRouter(
    prefix="/summary",
    tags=["Summary"]
)

# Adds sold player details to Summary model for transaction history and also updates both Teams and Players models
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TeamSummaryResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def player_sold_team(request:PlayerSoldRequest, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id, Auction.id == request.auction_id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access")
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


# Teams Summary to see which player they bought
@router.get('/team', status_code=status.HTTP_200_OK, response_model=TeamPlayerSummary, dependencies=[Depends(require_role(["team", "user"]))])
def team_summary(db: Session = Depends(get_db), user:TokenData=Depends(get_current_user)):
    team = db.query(Team).filter(Team.user_id == user.id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team Not Found")
    
    sold_players = db.query(Player)\
        .join(Summary, Summary.player_id == Player.id)\
        .filter(Summary.team_id == team.id)\
        .all()
    return TeamPlayerSummary(team=team, players=sold_players)

# Read Summay 
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=List[TeamSummaryResponse], dependencies=[Depends(require_role(["admin", "user"]))])
def get_summary(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id, Auction.id == id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    summary = db.query(Summary).filter(Summary.auction_id == id).all()
    if not summary:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found!")
    return summary


# Update Summary with team id
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=TeamPlayerSummary, dependencies=[Depends(require_role(["admin", "user"]))])
def update_summary(id:int, request:PlayerSoldRequest, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    summary = db.query(Summary).filter(Summary.id == id)
    player = db.query(Player).filter(Player.id == request.player_id).first()
    team = db.query(Team).filter(Team.id == request.team_id).first()
    if not summary.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Summary not found")
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
    summary.update(request.model_dump)
    player.sold_price = request.sold_price
    player.team_id = request.team_id
    team.remaining_purse -= request.sold_price
    db.commit()
    return summary