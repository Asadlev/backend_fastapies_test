from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from .models import Author
from .database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your_secret_key"


def create_access_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db = SessionLocal()
    user = db.query(Author).filter(Author.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user
