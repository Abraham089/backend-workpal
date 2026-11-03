from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import Annotated
from starlette import status
from datetime import timedelta
from backend_workpal.database.database import get_session
from .service import authenticate_user, create_access_token
from backend_workpal.core.config import settings

router = APIRouter(
  prefix="/auth",
  tags=["auth"],
  responses= {404: {"description": "not found"}}
)

@router.post("/token", status_code=status.HTTP_202_ACCEPTED)
async def login(
  response: Response,
  form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
  session: Annotated[Session, Depends(get_session)]
  ):
  user = authenticate_user(form_data.username, form_data.password, session)
  if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password",
                            headers={"WWW-Autenticate": "Bearer"})
  access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
  access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
  response.set_cookie(
      key="access_token",
      value=f"Bearer {access_token}",
      httponly=True,
      max_age=int(access_token_expires.total_seconds()),
      samesite="lax",
      secure=False,
      path="/"
  )
  return {"message": "Login successful"}
