from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.models import Auction, Team, Player
from ..db.connect import get_db
from ..auth.utils import require_role
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData

router = APIRouter(
    prefix='/dashboard',
    tags=['Auction Dashboard']
)

# Dashboard 
@router.get('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["user", "admin"]))])
def dashboard(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.id == id, Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    team =  db.query(Team).filter(Team.auction_id == id).all()
    player = db.query(Player).filter(Player.auction_id == id, Player.is_sold == False).all()

    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    
    return {"auction": auction, "teams": team, "players": player}
