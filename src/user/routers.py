from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import User
from .schemas import UserRequest, UserResponse

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# Create User
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(request:UserRequest, db:Session=Depends(get_db)):
    new_user = User(**request.model_dump())
    if not new_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Request")
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Read
@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    return user

# Update
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse)
def update_user(id:int, request:UserRequest, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    user.update(request.model_dump(), synchronize_session=False)
    db.commit()
    return user

# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK)
def delete_user(id:int, db:Session=Depends(get_db)):
    user = db.query(User).filter(User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    user.delete(synchronize_session=False)
    db.commit()
    return user
