from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

def hash_password(password:str):
    return pwd_context.hash(password)

def verify_password(hashed_password:str, passsword:str):
    return pwd_context.verify(hashed_password, passsword)