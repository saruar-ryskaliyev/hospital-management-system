from datetime import datetime, timedelta
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from .database import SessionLocal, get_db
from .models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

SECRET_KEY = "k43jnkn3j4n4j3nj4n3knkj4nfskfkweekf4"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


class CreateUserRequest(BaseModel):
    username: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


db_dependency = Annotated[Session, Depends(get_db)]





async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException( 
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    



@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):
    user = User(username=create_user_request.username,
                hashed_password=bcrypt_context.hash(create_user_request.password), role=create_user_request.role)

    if user.role not in ['admin', 'doctor', 'patient', 'staff']:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid role")
    db.add(user)
    db.commit()
    return {"username": user.username, "role": user.role}


@router.post("/admin/create_user", status_code=status.HTTP_201_CREATED)
async def admin_create_user(
    create_user_request: CreateUserRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != 'admin':
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions"
        )
    new_user = User(
        username=create_user_request.username,
        hashed_password=bcrypt_context.hash(create_user_request.password),
        role=create_user_request.role
    )

    if new_user.role not in ['admin', 'doctor', 'patient', 'staff']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role"
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "role": new_user.role}


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")
    token = create_access_token(user.username, user.id, timedelta(minutes=30))

    return {"access_token": token, "token_type": "bearer"}


def check_user_role(user: User, allowed_roles: list):
    if user.role not in allowed_roles:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Not enough permissions")

def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    to_encode = {"sub": username, "user_id": user_id}
    expires = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_current_active_user(allowed_roles: List[str]):
    async def _get_current_active_user(db: Session = Depends(get_db), token: str = Depends(oauth2_bearer)) -> User:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
            user = db.query(User).filter(User.username == username).first()
            if user is None:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
            if user.role not in allowed_roles:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not enough permissions")
            return user
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return _get_current_active_user
