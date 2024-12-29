from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import TeamResponseSchema, TeamCreateRequestSchema, TeamUpdateRequest
from ..db.connect import get_db
from ..db.models import Team, Auction
from sqlalchemy.orm import Session
from typing import List


router = APIRouter(
    prefix='/teams',
    tags=["Teams"]
)

# Create
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=TeamResponseSchema)
def create_team(request:TeamCreateRequestSchema, db:Session=Depends(get_db)):
    auction = db.query(Auction).filter(Auction.id == request.auction_id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Auction Not found")
    new_team = Team(remaining_purse=auction.purse_amt, **request.model_dump())
    if not new_team:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not created!")
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team

# Read
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[TeamResponseSchema])
def get_teams(db:Session=Depends(get_db), search:str="", limit:int=5, skip:int=0):
    teams = db.query(Team).filter(Team.name.contains(search)).limit(limit).offset(skip).all()
    if not teams:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Teams not found!")
    return teams

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=TeamResponseSchema)
def get_team_by_id(id:int, db:Session=Depends(get_db)):
    team = db.query(Team).filter(Team.id == id).first()
    if not team:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not found!")
    return team

# Update
@router.put('/{id}', status_code=status.HTTP_201_CREATED, response_model=TeamResponseSchema)
def update_team(id:int, request:TeamUpdateRequest, db:Session=Depends(get_db)):
    team = db.query(Team).filter(Team.id == id)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not found!")
    team.update(request.model_dump(), synchronize_session=False)
    db.commit()
    updated_team = team.first()
    return updated_team

# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_team(id:int, db:Session=Depends(get_db)):
    team = db.query(Team).filter(Team.id == id)
    if not team.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Team not found!")
    team.delete(synchronize_session=False)
    db.commit()
    return {"response":"Team Deleted Successfully!"}
