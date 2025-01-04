from fastapi import APIRouter, Depends, HTTPException, status
from ..db.connect import get_db
from ..db.models import User, Team
from sqlalchemy.orm import Session
from .utils import verify_password
from .oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .schemas import Token


router = APIRouter(
    prefix='/login',
    tags=["Authentication"]
)


# Login using jwt
@router.post('/', status_code=status.HTTP_200_OK, response_model=Token)
def user_login(request:OAuth2PasswordRequestForm=Depends(), db:Session=Depends(get_db)):
    user = db.query(User).filter(User.username == request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!")
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials!")
    data = {"user_id":user.id, "user_role":user.role}
    jwt_token = create_access_token(data)
    return {"access_token":jwt_token, "token_type":"bearer"}
