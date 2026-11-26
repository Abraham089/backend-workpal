from sqlmodel import Session
from datetime import date, timedelta

from fastapi.testclient import TestClient
from backend_workpal.database.database import save
from backend_workpal.api.v1.users.models import UserSummary, UserCreate
from backend_workpal.api.v1.roles.models import Roles
from backend_workpal.api.v1.projects.models import Projects, ProjectCreate, ProjectUpdate, ProjectResponse, ProjectSummary
from backend_workpal.api.v1.project_members.models import ProjectMemberCreate, ProjectMemberResponse, ProjectMemberUpdate
from backend_workpal.api.v1.project_join_requests.models import ProjectJoinRequestCreate, ProjectJoinRequestUpdate, JoinRequestStatus

ENDING_DATE = date.today() + timedelta(days=30)

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

def test_post_project(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_response.status_code == 201

  project_data = ProjectResponse.model_validate(project_response.json())
  assert project_data.id == 1
  assert project_data.name == "Example Project"
  assert project_data.created_by == user_data
  assert project_data.supervisor_user is None
  assert len(project_data.members) == 1
  assert project_data.members[0].user == user_data
  assert project_data.members[0].is_leader is True

def test_post_member_to_project(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  rol = Roles(name= "example rol")
  saved_rol = save(session, rol)

  user_2 = UserCreate(
    name="example name 2",
    last_name="example last name 2",
    username="example1234",
    mail="examplemail2@gmail.com",
    is_active=True,
    password="example_password123",
    role_id=saved_rol.id
  )
  
  user_2_response = client.post("/v1/users/", json=user_2.model_dump())
  user_2_data = UserSummary.model_validate(user_2_response.json())

  assert user_2_response.status_code == 201

  new_project_member = ProjectMemberCreate(
    can_edit_project_details= False,
    can_manage_tasks= True,
    can_delete_tasks= False,
    can_invite_members= False,
    is_leader= False,
    user_id= user_2_data.id
  )

  project_member_response = client.post("/v1/projects/1/members/", json=new_project_member.model_dump(mode="json"))
  assert project_member_response.status_code == 201
  assert project_member_response.json() is True

  duplicate_response = client.post(
      "/v1/projects/1/members/", json=new_project_member.model_dump(mode="json")
  )
  assert duplicate_response.status_code == 400

def test_post_join_request(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  project_join_request_create = ProjectJoinRequestCreate(message="Example message")

  join_request_response = client.post("/v1/projects/1/join_request/", json=project_join_request_create.model_dump(mode="json"))
  assert join_request_response.status_code == 400

  user_data = _create_and_login_user(client, session,rol="Example rol", username="example 2", mail="examplemail2@gmail.com")

  join_request_response = client.post("/v1/projects/1/join_request/", json=project_join_request_create.model_dump(mode="json"))
  assert join_request_response.status_code == 202

def test_read_join_requests_by_project_id(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  project_join_request_create = ProjectJoinRequestCreate(message="Example message")

  user_data = _create_and_login_user(client, session,rol="Example rol", username="example 2", mail="examplemail2@gmail.com")

  join_request_response = client.post("/v1/projects/1/join_request/", json=project_join_request_create.model_dump(mode="json"))
  assert join_request_response.status_code == 202

  login_data = {
    "username": "example123",
    "password": "example_password123"
  }
    
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  join_requests_response = client.get("/v1/projects/1/join_requests/")
  assert join_requests_response.status_code == 202

  data = join_requests_response.json()
  assert len(data) > 0

def test_read_projects(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  read_project_response = client.get("/v1/projects/")

  assert read_project_response.status_code == 202
  data = read_project_response.json()
  assert len(data) > 0

def test_read_project_by_id(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  read_project_by_id_response = client.get("/v1/projects/1")

  assert read_project_by_id_response.status_code == 202

  project_data = ProjectResponse.model_validate(read_project_by_id_response.json())
  assert project_data.id == 1
  assert project_data.created_by == user_data
  assert len(project_data.members) == 1

def test_read_all_project_members_in_project(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)
  
  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )
  
  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  project_summary = ProjectSummary.model_validate(project_create_response.json())

  project_members_response = client.get("/v1/projects/1/project_members/")
  assert project_members_response.status_code == 200

  new_member_data = ProjectMemberResponse(
    id=1,
    can_edit_project_details= True,
    can_manage_tasks= True,
    can_delete_tasks= True,
    can_invite_members= True,
    is_leader= True,
    user=user_data,
    project=project_summary
    )

  data = project_members_response.json()
  assert data == [new_member_data.model_dump(mode="json")]

def test_read_project_member_by_project_and_member_id(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)
    
  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )
    
  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  project_summary = ProjectSummary.model_validate(project_create_response.json())

  project_member_response = client.get("/v1/projects/1/project_member/1")
  assert project_member_response.status_code == 200

  new_member_data = ProjectMemberResponse(
    id=1,
    can_edit_project_details= True,
    can_manage_tasks= True,
    can_delete_tasks= True,
    can_invite_members= True,
    is_leader= True,
    user=user_data,
    project=project_summary
  )

  data = project_member_response.json()
  assert data == new_member_data.model_dump(mode="json")

def test_put_project(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  updated_project = ProjectUpdate(
      name="Example Project 2",
      description="Example description",
      img="img example",
      status="Active",
      created_by_id=user_data.id,
      created_at=new_project.created_at,
      ending_date=ENDING_DATE
    )

  put_project_response = client.put("/v1/projects/1", json=updated_project.model_dump(mode="json"))

  assert put_project_response.status_code == 202

  project_data = ProjectResponse.model_validate(put_project_response.json())
  assert project_data.name == "Example Project 2"
  assert project_data.created_by == user_data

def test_put_project_member(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)
  
  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )
  
  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201
  
  rol = Roles(name= "example rol")
  saved_rol = save(session, rol)
  
  user_2 = UserCreate(
    name="example name 2",
    last_name="example last name 2",
    username="example1234",
    mail="examplemail2@gmail.com",
    is_active=True,
    password="example_password123",
    role_id=saved_rol.id
  )
    
  user_2_response = client.post("/v1/users/", json=user_2.model_dump())
  user_2_data = UserSummary.model_validate(user_2_response.json())
  
  assert user_2_response.status_code == 201
  
  new_project_member = ProjectMemberCreate(
    can_edit_project_details= False,
    can_manage_tasks= True,
    can_delete_tasks= False,
    can_invite_members= False,
    is_leader= False,
    user_id= user_2_data.id
  )
  
  project_member_response = client.post("/v1/projects/1/members/", json=new_project_member.model_dump(mode="json"))
  assert project_member_response.status_code == 201

  new_member_data = ProjectMemberUpdate(
    can_delete_tasks=True,
    can_edit_project_details=True,
    can_invite_members=False,
    can_manage_tasks=True
  )

  project_member_response = client.put("/v1/projects/1/project_member/1/", json=new_member_data.model_dump(mode="json"))
  assert project_member_response.status_code == 403

  project_member_response = client.put("/v1/projects/1/project_member/999/", json=new_member_data.model_dump(mode="json"))
  assert project_member_response.status_code == 404

  project_member_response = client.put("/v1/projects/1/project_member/2/", json=new_member_data.model_dump(mode="json"))
  assert project_member_response.status_code == 202

  data = project_member_response.json()
  new_project_member_data = ProjectMemberResponse.model_validate(data)
  assert data == new_project_member_data.model_dump(mode="json")

  assert new_project_member_data.can_edit_project_details == new_member_data.can_edit_project_details

def test_update_project_join_request(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  project_summary = ProjectSummary.model_validate(project_create_response.json())

  project_join_request_create = ProjectJoinRequestCreate(message="Example message")

  user_1_data = _create_and_login_user(client, session,rol="Example rol", username="example 2", mail="examplemail2@gmail.com")

  join_request_response_1 = client.post("/v1/projects/1/join_request/", json=project_join_request_create.model_dump(mode="json"))
  assert join_request_response_1.status_code == 202

  user_2_data = _create_and_login_user(client, session,rol="Example rol 2", username="example 3", mail="examplemail3@gmail.com")

  join_request_response_2 = client.post("/v1/projects/1/join_request/", json=project_join_request_create.model_dump(mode="json"))
  assert join_request_response_2.status_code == 202
  
  login_data = {
    "username": "example123",
    "password": "example_password123"
  }
      
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  update_status = ProjectJoinRequestUpdate(status=JoinRequestStatus.ACCEPTED)

  join_request_response = client.put("/v1/projects/1/join_request/1", json=update_status.model_dump(mode="json"))
  assert join_request_response.status_code == 202

  data = join_request_response.json()
  assert data == {
    "id": 1,
    "message": project_join_request_create.message,
    "status": update_status.status.value,
    "created_at": date.today().isoformat(),
    "user": user_1_data.model_dump(mode="json"),
    "project": project_summary.model_dump(mode="json")
  }

  update_status = ProjectJoinRequestUpdate(status=JoinRequestStatus.REJECTED)
  
  join_request_response = client.put("/v1/projects/1/join_request/2", json=update_status.model_dump(mode="json"))
  assert join_request_response.status_code == 202
  
  data = join_request_response.json()
  assert data == {
    "id": 2,
    "message": project_join_request_create.message,
    "status": update_status.status.value,
    "created_at": date.today().isoformat(),
    "user": user_2_data.model_dump(mode="json"),
    "project": project_summary.model_dump(mode="json")
  }

def test_delete_project(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )

  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201

  delete_project_response = client.delete("/v1/projects/999")
  
  assert delete_project_response.status_code == 404

  delete_project_response = client.delete("/v1/projects/1")

  assert delete_project_response.status_code == 200
  data = delete_project_response.json()
  assert data == 1

def test_delete_project_member(client: TestClient, session: Session):
  user_data = _create_and_login_user(client, session)

  new_project = ProjectCreate(
    name="Example Project",
    description="Example description",
    img="img example",
    status="Active",
    created_by_id=user_data.id,
    ending_date=ENDING_DATE
  )
  
  project_create_response = client.post("/v1/projects/", json=new_project.model_dump(mode="json"))
  assert project_create_response.status_code == 201
  
  rol = Roles(name= "example rol")
  saved_rol = save(session, rol)
  
  user_2 = UserCreate(
    name="example name 2",
    last_name="example last name 2",
    username="example1234",
    mail="examplemail2@gmail.com",
    is_active=True,
    password="example_password123",
    role_id=saved_rol.id
  )
    
  user_2_response = client.post("/v1/users/", json=user_2.model_dump())
  user_2_data = UserSummary.model_validate(user_2_response.json())
  
  assert user_2_response.status_code == 201
  
  new_project_member = ProjectMemberCreate(
    can_edit_project_details= False,
    can_manage_tasks= True,
    can_delete_tasks= False,
    can_invite_members= False,
    is_leader= False,
    user_id= user_2_data.id
  )
  
  project_member_response = client.post("/v1/projects/1/members/", json=new_project_member.model_dump(mode="json"))
  assert project_member_response.status_code == 201

  login_data = {
    "username": "example123",
    "password": "example_password123"
  }
      
  login_response = client.post("/v1/auth/token", data=login_data)
  assert login_response.status_code == 202

  project_member_delete_response = client.delete("/v1/projects/1/project_member/999")
  assert project_member_delete_response.status_code == 404

  project_member_delete_response = client.delete("/v1/projects/1/project_member/1")
  assert project_member_delete_response.status_code == 403

  project_member_delete_response = client.delete("/v1/projects/1/project_member/2")
  assert project_member_delete_response.status_code == 202

  data = project_member_delete_response.json()
  assert data == True
