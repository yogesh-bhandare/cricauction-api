from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import Auction, Team, Player, User
from .schemas import AuctionRequestSchema, AuctionResponseSchema
from typing import List, Optional
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData
from ..auth.utils import require_role
from ..auth.schemas import TokenData
from ..auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/auctions',
    tags=['Auctions']
)

# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AuctionResponseSchema, dependencies=[Depends(require_role(["admin", "user"]))])
def create_auction(request:AuctionRequestSchema, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    is_user = db.query(User).filter(User.id == user.id).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Access")
    new_auction = Auction(user_id=user.id, **request.model_dump())
    if not new_auction:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Auction not created!")
    db.add(new_auction)
    db.commit()
    db.refresh(new_auction)
    return new_auction

# Read
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[AuctionResponseSchema], dependencies=[Depends(require_role(["admin", "user"]))])
def get_auction(db:Session=Depends(get_db), user:TokenData=Depends(get_current_user), search:Optional[str]="", limit:int=5, skip:int=0):
    is_user = db.query(User).filter(User.id == user.id).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Access")
    auctions = db.query(Auction).filter(Auction.user_id == user.id, Auction.name.contains(search)).limit(limit).offset(skip).all()
    if not auctions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    return auctions

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AuctionResponseSchema, dependencies=[Depends(require_role(["admin", "user"]))])
def get_auction_by_id(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    is_user = db.query(User).filter(User.id == user.id).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Access")
    auction = db.query(Auction).filter(Auction.id == id, Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    return auction


# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=AuctionResponseSchema, dependencies=[Depends(require_role(["admin", "user"]))])
def update_auction(id:int, request:AuctionRequestSchema, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    is_user = db.query(User).filter(User.id == user.id).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Access")
    auction = db.query(Auction).filter(Auction.id == id, Auction.user_id == user.id)
    if not auction.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    auction.update(request.model_dump(), synchronize_session=False)
    db.commit()
    updated_auction = auction.first()
    return updated_auction


# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["admin", "user"]))])
def delete_auction(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    is_user = db.query(User).filter(User.id == user.id).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Access")
    auction = db.query(Auction).filter(Auction.id == id, Auction.user_id == user.id)
    if not auction.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Auction details not found!")
    auction.delete(synchronize_session=False)
    db.commit()
    return {"response":f"Auction {id} deleted successfully!"}
