from sqlmodel import Session
from fastapi.testclient import TestClient
from backend_workpal.database.database import save
from backend_workpal.api.v1.users.models import Users, UserCreate
from backend_workpal.api.v1.roles.models import Roles, RoleCreate
from backend_workpal.core.security import get_password_hash

def test_get_roles(client: TestClient, session: Session):
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
  
  login_data = {
    "username": "example123",
    "password": "example_password123"
  }
  
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  response = client.get("/v1/roles/")

  assert response.status_code == 202
  data = response.json()
  assert len(data) > 0

def test_get_role_by_id(client: TestClient, session: Session):
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
  
  login_data = {
    "username": "example123",
    "password": "example_password123"
  }
  
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  response = client.get("/v1/roles/1")

  assert response.status_code == 202
  data = response.json()
  assert data == {
    "id": 1,
    "name": "admin"
    }

def test_post_role(client: TestClient, session: Session):
  rol = Roles(name= "admin")
  saved_rol = save(session, rol)
    
  user = UserCreate(
    name="example name",
    last_name="example last name",
    username="example123",
    mail="examplemail@gmail.com",
    is_active=True,
    password="example_password123",
    role_id=saved_rol.id
  )

  response = client.post("/v1/users/", json=user.model_dump())

  assert response.status_code == 201

  login_data = {
      "username": "example123",
      "password": "example_password123"
    }

  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  new_role = RoleCreate(
    name="new Example Role"
  )

  response = client.post("/v1/roles/", json=new_role.model_dump())
  assert response.status_code == 201
  data = response.json()
  assert data == {
    "id": 2,
    "name": "new Example Role"
  }
