from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db.connect import get_db
from ..db.models import User
from .schemas import UserRequest, UserResponse
from ..auth.utils import hash_password
from typing import List
from ..auth.utils import require_role

router = APIRouter(
    prefix='/signup',
    tags=['Signup']
)

# Create User
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(request:UserRequest, db:Session=Depends(get_db)):
    try:
        password = request.password
        request.password = hash_password(password)
        new_user = User(**request.model_dump())
        if not new_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Failed to create user. Please check your input data.")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return new_user

# Read
@router.get('/', status_code=status.HTTP_200_OK, response_model=List[UserResponse], dependencies=[Depends(require_role(["admin", "team", "user"]))])
def get_user(db:Session=Depends(get_db)):
    try:
        user = db.query(User).all()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return user

@router.get('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def get_user(id:int, db:Session=Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return user

# Update
@router.put('/{id}', status_code=status.HTTP_200_OK, response_model=UserResponse, dependencies=[Depends(require_role(["admin", "user"]))])
def update_user(id:int, request:UserRequest, db:Session=Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
        user.update(request.model_dump(), synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return user

# Delete
@router.delete('/{id}', status_code=status.HTTP_200_OK, dependencies=[Depends(require_role(["admin", "user"]))])
def delete_user(id:int, db:Session=Depends(get_db)):
    try:
        user = db.query(User).filter(User.id == id)
        if not user.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
        user.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected error occurred!")
    return user
