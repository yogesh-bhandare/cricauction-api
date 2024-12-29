from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import Auction, Team, Player
from .schemas import AuctionRequestSchema, AuctionResponseSchema
from typing import List, Optional


router = APIRouter(
    prefix='/auctions',
    tags=['Auctions']
)

# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AuctionResponseSchema)
def create_auction(request:AuctionRequestSchema, db:Session=Depends(get_db)):
    new_auction = Auction(**request.model_dump())
    if not new_auction:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Auction not created!")
    db.add(new_auction)
    db.commit()
    db.refresh(new_auction)
    return new_auction

# Read
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[AuctionResponseSchema])
def get_auction(db:Session=Depends(get_db), search:Optional[str]="", limit:int=5, skip:int=0):
    auctions = db.query(Auction).filter(Auction.name.contains(search)).limit(limit).offset(skip).all()
    if not auctions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    return auctions

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AuctionResponseSchema)
def get_auction_by_id(id:int, db:Session=Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    return auction

# Dashboard 
@router.get('/dashboard/{id}', status_code=status.HTTP_200_OK)
def dashboard(id:int, db:Session=Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == id).first()
    team =  db.query(Team).filter(Team.auction_id == id).all()
    player = db.query(Player).filter(Player.auction_id == id, Player.is_sold == False).all()

    if not auction:
        raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="Auction not found!")
    if not team:
        raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="Team not found!")
    if not player:
        raise HTTPException(status_code=status.HTTP_404_BAD_REQUEST, detail="Player not found!")
    
    return {"auction": auction, "teams": team, "players": player}

# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=AuctionResponseSchema)
def update_auction(id:int, request:AuctionRequestSchema, db:Session=Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == id)
    if not auction.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    auction.update(request.model_dump(), synchronize_session=False)
    db.commit()
    updated_auction = auction.first()
    return updated_auction



# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_auction(id:int, db:Session=Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == id)
    if not auction.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    auction.delete(synchronize_session=False)
    db.commit()
    return {"response":f"Auction {id} deleted successfully!"}
