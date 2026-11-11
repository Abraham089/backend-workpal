from sqlmodel import Session
from fastapi.testclient import TestClient
from backend_workpal.database.database import save
from backend_workpal.api.v1.users.models import Users
from backend_workpal.api.v1.skills.models import Skills
from backend_workpal.api.v1.roles.models import Roles
from backend_workpal.core.security import get_password_hash

def test_get_skills(client: TestClient, session: Session):
  rol = Roles(name= "admin")
  saved_rol = save(session, rol)
  
  hashed_password = get_password_hash("example_password123")
    
  user = Users(
    name="example name",
    last_name="example last name",
    username="example123",
    mail="examplemail@gmail.com",
    password_hash= hashed_password,
    is_active=True,
    role_id= saved_rol.id)
  saved_user=save(session, user)

  skill = Skills(
    name="example skill"
  )
  saved_skill=save(session, skill)
  
  login_data = {
    "username": "example123",
    "password": "example_password123"
  }
  
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  response = client.get("/v1/skills/")

  assert response.status_code == 202
  data = response.json()
  assert len(data) > 0

def test_get_skill_by_id(client: TestClient, session: Session):
  rol = Roles(name= "admin")
  saved_rol = save(session, rol)
  
  hashed_password = get_password_hash("example_password123")
    
  user = Users(
    name="example name",
    last_name="example last name",
    username="example123",
    mail="examplemail@gmail.com",
    password_hash= hashed_password,
    is_active=True,
    role_id= saved_rol.id)
  saved_user = save(session, user)

  skill = Skills(
    name="example skill"
  )
  saved_skill=save(session, skill)
  
  login_data = {
    "username": "example123",
    "password": "example_password123"
  }
  
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  response = client.get("/v1/skills/1")

  assert response.status_code == 202
  data = response.json()
  assert data == {
    "id": 1,
    "name": "example skill"
  }
