from sqlmodel import Session
from datetime import date

from fastapi.testclient import TestClient
from backend_workpal.database.database import save
from backend_workpal.api.v1.users.models import UserResponse, UserCreate
from backend_workpal.api.v1.roles.models import Roles
from backend_workpal.api.v1.projects.models import Projects, ProjectCreate
from backend_workpal.core.security import get_password_hash

def test_post_project(client: TestClient, session: Session):
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

  user_response = client.post("/v1/users/", json=user.model_dump())
  user_data = UserResponse.model_validate(user_response.json())

  assert user_response.status_code == 201

  login_data = {
      "username": "example123",
      "password": "example_password123"
    }

  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=date(2026, 11, 7)
  )

  project_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_response.status_code == 201
  data = project_response.json()
  assert data == {
    "id": 1,
    "name": "Example Project",
    "description": "Example description",
    "img": "img example",
    "status": "Active",
    "created_by": user_data.model_dump(),
    "supervisor_user": None,
    "created_at": date.today().isoformat(),
    "ending_date": date(2026, 11, 7).isoformat(),
  }

def test_read_projects(client: TestClient, session: Session):
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

  user_response = client.post("/v1/users/", json=user.model_dump())
  user_data = UserResponse.model_validate(user_response.json())

  assert user_response.status_code == 201

  login_data = {
      "username": "example123",
      "password": "example_password123"
    }

  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=date(2026, 11, 7)
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  read_project_response = client.get("/v1/projects/")

  assert read_project_response.status_code == 202
  data = read_project_response.json()
  assert len(data) > 0

def test_read_project_by_id(client: TestClient, session: Session):
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

  user_response = client.post("/v1/users/", json=user.model_dump())
  user_data = UserResponse.model_validate(user_response.json())

  assert user_response.status_code == 201

  login_data = {
      "username": "example123",
      "password": "example_password123"
    }

  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=date(2026, 11, 7)
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  read_project_by_id_response = client.get("/v1/projects/1")

  assert read_project_by_id_response.status_code == 202
  data = read_project_by_id_response.json()
  assert data == {
    "id": 1,
    "name": "Example Project",
    "description": "Example description",
    "img": "img example",
    "status": "Active",
    "created_by": user_data.model_dump(),
    "supervisor_user": None,
    "created_at": date.today().isoformat(),
    "ending_date": date(2026, 11, 7).isoformat(),
  }
