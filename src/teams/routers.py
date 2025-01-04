from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import TeamResponseSchema, TeamCreateRequestSchema, TeamUpdateRequest, TeamRequest
from ..db.connect import get_db
from ..db.models import Team, Auction, User
from sqlalchemy.orm import Session
from typing import List
from ..auth.utils import require_role, hash_password
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData


router = APIRouter(
    prefix='/teams',
    tags=["Teams"]
)

# Create
@router.post('/{id}', status_code=status.HTTP_201_CREATED, response_model=TeamResponseSchema, dependencies=[Depends(require_role(["admin", "user"]))])
def create_team(id:int, request:TeamRequest, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id, Auction.id == id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Auction")

    password = request.password
    request.password = hash_password(password)
    new_user = User(**request.model_dump())
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Request")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_team = Team(name=new_user.username, user_id=new_user.id, auction_id=id, remaining_purse=auction.purse_amt)
    if not new_team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not created!")
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

# Read
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=List[TeamResponseSchema], dependencies=[Depends(require_role(["admin", "user"]))])
def get_teams(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user), search:str="", limit:int=5, skip:int=0):
    auction = db.query(Auction).filter(Auction.user_id == user.id, Auction.id == id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    teams = db.query(Team).filter(Team.auction_id == id, Team.name.contains(search)).limit(limit).offset(skip).all()
    if not teams:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teams not found!")
    return teams

@router.get('/by/{id}', status_code=status.HTTP_200_OK, response_model=TeamResponseSchema, dependencies=[Depends(require_role(["admin", "user"]))])
def get_team_by_id(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    team = db.query(Team).filter(Team.id == id, Team.auction_id == Auction.id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
    return team

# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=TeamResponseSchema, dependencies=[Depends(require_role(["admin", "user"]))])
def update_team(id:int, request:TeamUpdateRequest, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    team = db.query(Team).filter(Team.id == id, Team.auction_id == Auction.id)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
    team.update(request.model_dump(), synchronize_session=False)
    db.commit()
    updated_team = team.first()
    return updated_team

# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["admin", "user"]))])
def delete_team(id:int, db:Session=Depends(get_db), user:TokenData=Depends(get_current_user)):
    auction = db.query(Auction).filter(Auction.user_id == user.id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Access!")
    team = db.query(Team).filter(Team.id == id, Team.auction_id == Auction.id)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Team not found!")
    team.delete(synchronize_session=False)
    db.commit()
    return {"response":"Team Deleted Successfully!"}
