from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import Auction
from .schemas import AuctionRequest, AuctionResponse
from typing import List, Optional
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData
from ..auth.utils import require_role, verify_user_access
from ..auth.schemas import TokenData
from ..auth.oauth2 import get_current_user


router = APIRouter(
    prefix='/auctions',
    tags=['Auctions']
)


# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AuctionResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def create_auction(request:AuctionRequest, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        verify_user_access(db, current_user.id)
        new_auction = Auction(user_id=current_user.id, **request.model_dump())
        if not new_auction:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Not created!")
        db.add(new_auction)
        db.commit()
        db.refresh(new_auction)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {e}")
    return new_auction


# Read
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[AuctionResponse], dependencies=[Depends(require_role(["admin", "user"]))])
def get_auction(db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user), search:Optional[str]="", limit:int=5, skip:int=0):
    try:
        verify_user_access(db, current_user.id)
        auctions = db.query(Auction).filter(Auction.user_id == current_user.id, Auction.name.contains(search)).limit(limit).offset(skip).all()
        if not auctions:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {e}")
    return auctions


@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=AuctionResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def get_auction_by_id(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        verify_user_access(db, current_user.id)
        auction = db.query(Auction).filter(Auction.id == id, Auction.user_id == current_user.id).first()
        if not auction:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {e}")
    return auction


# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=AuctionResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def update_auction(id:int, request:AuctionRequest, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        verify_user_access(db, current_user.id)
        auction = db.query(Auction).filter(Auction.id == id, Auction.user_id == current_user.id)
        if not auction.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
        auction.update(request.model_dump(), synchronize_session=False)
        db.commit()
        updated_auction = auction.first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {e}")
    return updated_auction


# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["admin", "user"]))])
def delete_auction(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        verify_user_access(db, current_user.id)
        auction = db.query(Auction).filter(Auction.id == id, Auction.user_id == current_user.id)
        if not auction.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found!")
        auction.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error occurred: {e}")
    return {"response":"Successful!"}
