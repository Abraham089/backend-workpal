from sqlmodel import Session, select, col
from sqlalchemy.orm import joinedload
from .models import Users, UserCreate
from typing import List
from backend_workpal.database.database import save
from backend_workpal.core.security import get_password_hash

class UserService:
  def read_user_by_id(self, user_id:int, session: Session):
    statement = select(Users).where(Users.id == user_id).options(joinedload(Users.role))
    user = session.exec(statement).first()
    
    return user

  def read_user_by_username(self, username:str, session: Session):
      statement = select(Users).where(Users.username == username)
      user = session.exec(statement).first()
      
      return user

  def read_all_users(self, session: Session):
    users = select(Users).options(joinedload(Users.role))
    return session.exec(users).all()

  def create_user(self, new_user_data: UserCreate, hashed_password: str, session: Session):
    new_user = Users(
      enrollment=new_user_data.enrollment,
      name=new_user_data.name,
      last_name=new_user_data.last_name,
      username=new_user_data.username,
      mail=new_user_data.mail,
      password_hash=hashed_password,
      role_id=new_user_data.role_id
    )

    saved_user = save(session, new_user)

    return saved_user