from fastapi import APIRouter, Depends, HTTPException, status


router = APIRouter(
    prefix='/login',
    tags=["Authentication"]
)


# Login using jwt
@router.post('/', status_code=status.HTTP_200_OK)
def user_login():
    return