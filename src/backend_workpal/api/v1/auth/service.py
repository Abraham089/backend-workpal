from fastapi import Depends, HTTPException, status, Cookie
from sqlmodel import Session
import urllib.parse
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from datetime import timedelta, datetime, timezone
from backend_workpal.core.security import verify_password, DUMMY_HASH
from backend_workpal.core.config import settings
from .models import TokenData
from ..users.service import UserService
from backend_workpal.database.database import get_session

user_service = UserService()

def authenticate_user(username: str, password: str, session: Session):
    user = user_service.read_user_by_username(username, session)
    if not user:
        verify_password(password, DUMMY_HASH)
        return False
    correct_password = verify_password(password, user.password_hash)
    if not correct_password:
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expires_delta = expires_delta if expires_delta else timedelta(minutes=15)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(session: Annotated[Session, Depends(get_session)], access_token: Annotated[str | None, Cookie()] = None): # pragma: no cover
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate crerdentials"
    )
    if not access_token:
       raise credentials_exception
    try:
        raw_token = urllib.parse.unquote(access_token)
        cleaned_token = raw_token.strip(' "\'')
        token_type, token = cleaned_token.split(" ")
        if token_type.lower() != "bearer":
           raise credentials_exception
    except ValueError:
       raise credentials_exception
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = user_service.read_user_by_username(token_data.username, session)
    if user is None:
        raise credentials_exception
    return user
