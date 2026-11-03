from sqlmodel import Session
from fastapi.testclient import TestClient
from backend_workpal.database.database import save
from backend_workpal.api.v1.users.models import Users
from backend_workpal.api.v1.roles.models import Roles
from backend_workpal.core.security import get_password_hash

def test_login(client: TestClient, session: Session):
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

  response = client.post("/v1/auth/token", data=login_data)

  assert response.status_code == 202
  assert response.json() == {"message": "Login successful"}
  assert "access_token" in response.cookies
