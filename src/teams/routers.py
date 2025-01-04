from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import TeamResponse, TeamUpdateRequest, TeamRequest
from ..db.connect import get_db
from ..db.models import Team, Auction, User
from sqlalchemy.orm import Session
from typing import List
from ..auth.utils import require_role, hash_password, verify_auction_access
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData


router = APIRouter(
    prefix='/teams',
    tags=["Teams"]
)


# Create
@router.post('/{id}', status_code=status.HTTP_201_CREATED, response_model=TeamResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def create_team(id:int, request:TeamRequest, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        auction = verify_auction_access(db, current_user.id, id)
        password = request.password
        request.password = hash_password(password)
        new_user = User(**request.model_dump())
        if not new_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Input!")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        new_team = Team(name=new_user.username, user_id=new_user.id, auction_id=id, remaining_purse=auction.purse_amt)
        if not new_team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not created!")
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return new_team


# Read
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=List[TeamResponse], dependencies=[Depends(require_role(["admin", "user"]))])
def get_teams(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user), search:str="", limit:int=5, skip:int=0):
    try:
        teams = db.query(Team).filter(Team.auction_id == id, Team.name.contains(search)).limit(limit).offset(skip).all()
        if not teams:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teams not found!")
        verify_auction_access(db, current_user.id, id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return teams


@router.get('/by/{id}', status_code=status.HTTP_200_OK, response_model=TeamResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def get_team_by_id(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        team = db.query(Team).filter(Team.id == id, Team.auction_id == Auction.id).first()
        if not team:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
        verify_auction_access(db, current_user.id, team.auction_id)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return team


# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=TeamResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def update_team(id:int, request:TeamUpdateRequest, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        team = db.query(Team).filter(Team.id == id, Team.auction_id == Auction.id)
        if not team.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
        verify_auction_access(db, current_user.id, team.first().auction_id)
        team.update(request.model_dump(), synchronize_session=False)
        db.commit()
        updated_team = team.first()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return updated_team


# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["admin", "user"]))])
def delete_team(id:int, db:Session=Depends(get_db), current_user:TokenData=Depends(get_current_user)):
    try:
        team = db.query(Team).filter(Team.id == id, Team.auction_id == Auction.id)
        if not team.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
        verify_auction_access(db, current_user.id, team.first().auction_id)
        team.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return {"response":"Team Deleted Successfully!"}
