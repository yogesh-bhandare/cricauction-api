from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.models import Auction, Team, Player
from ..db.connect import get_db
from ..auth.utils import require_role, verify_auction_access
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData

router = APIRouter(
    prefix='/dashboard',
    tags=['Auction Dashboard']
)

# Dashboard 
@router.get('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["user", "admin"]))])
def dashboard(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        auction = verify_auction_access(db, current_user.id, id)
        teams =  db.query(Team).filter(Team.auction_id == id).all()
        players = db.query(Player).filter(Player.auction_id == id, Player.is_sold == False).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")

    if not teams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
    if not players:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found!")
    
    return {"auction": auction, "teams": teams, "players": players}
