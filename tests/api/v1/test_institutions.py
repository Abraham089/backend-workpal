from sqlmodel import Session
from fastapi.testclient import TestClient
from backend_workpal.api.v1.roles.models import Roles
from backend_workpal.api.v1.users.models import UserSummary, UserCreate
from backend_workpal.api.v1.institutions.models import InstitutionCreate, InstitutionResponse
from backend_workpal.database.database import save

def _create_and_login_user(
    client: TestClient,
    session: Session,
    rol: str = "admin",
    username: str = "example123",
    mail: str = "examplemail@gmail.com",
    password: str = "example_password123",
):
  rol = Roles(name=rol)
  saved_rol = save(session, rol)
      
  user = UserCreate(
    name="example name",
    last_name="example last name",
    username=username,
    mail=mail,
    is_active=True,
    password=password,
    role_id=saved_rol.id
  )
  
  user_response = client.post("/v1/users/", json=user.model_dump())
  user_data = UserSummary.model_validate(user_response.json())
  
  assert user_response.status_code == 201
  
  login_data = {
      "username": username,
      "password": password
    }
  
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  return user_data

def test_post_institution(client: TestClient, session: Session):
  _create_and_login_user(client=client, session=session, rol="Admin")

  new_institution = InstitutionCreate(
    name="Example institution",
    description="Example",
    color="fafafa",
    logo="Example logo"
  )

  new_institution_response = client.post("/v1/institutions/", json=new_institution.model_dump(mode="json"))
  assert new_institution_response.status_code == 201

  data = new_institution_response.json()
  new_institution = InstitutionResponse.model_validate(data)
  assert new_institution.id == 1
  assert new_institution.name == "Example institution"
  assert new_institution.description == "Example"
  assert new_institution.color == "fafafa"
  assert new_institution.logo =="Example logo"
  assert new_institution.users == []

  _create_and_login_user(client=client, session=session, username="example1234", mail="examplemail2@gmail.com", rol="no admin")