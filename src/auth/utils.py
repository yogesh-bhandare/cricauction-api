from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from ..auth.oauth2 import get_current_user
from ..auth.schemas import TokenData
from sqlalchemy.orm import Session
from ..db.models import User, Auction

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(passsword:str, hashed_password:str):
    return pwd_context.verify(passsword, hashed_password)

def require_role(allowed_roles:list[str]):
    def roles_dependency(user:TokenData=Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied for role.")
    return roles_dependency

def verify_user_access(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    return user

def verify_auction_access(db:Session, user_id:int, auction_id:int):
    auction = db.query(Auction).filter(Auction.user_id == user_id, Auction.id == auction_id).first()
    if not auction:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized access")
    return auction
