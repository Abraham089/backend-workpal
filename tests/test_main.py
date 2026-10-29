import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from src.backend_workpal.database.database import save
from src.backend_workpal.api.v1.task_with_skill.models import TaskWithSkill
from src.backend_workpal.api.v1.tasks.models import Tasks
from src.backend_workpal.api.v1.skills.models import Skills
from src.backend_workpal.api.v1.users.models import Users
from src.backend_workpal.api.v1.projects.models import Projects
from src.backend_workpal.api.v1.roles.models import Roles

@pytest.fixture(name="session")
def session_fixture():
  engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass= StaticPool
  )
  SQLModel.metadata.create_all(engine)
  with Session(engine) as session:
    yield session

def test_create_things_in_db(session: Session):
  rol = Roles(name= "admin")
  saved_rol = save(session, rol)

  user = Users(password_hash= "example123", role_id= 1)
  saved_user = save(session, user)

  project = Projects(
    name= "Example Project",
    description= "Example description",
    img= "img example",
    user_leader_id= "1")
  saved_project = save(session, project)

  skill = Skills(name="Example skill")
  saved_skill = save(session, skill)

  task = Tasks(
    name= "Example Task",
    description= "Example description",
    status= "Ok",
    project_id= "1",
    user_id= 1)
  saved_task = save(session, task)

  task_with_skill = TaskWithSkill(task_id=1, skill_id=1)
  saved_task_with_skill = save(session, task_with_skill)

  rol_ressult = session.exec(select(Roles))
  user_ressult = session.exec(select(Users))
  project_ressult = session.exec(select(Projects))
  skill_ressult = session.exec(select(Skills))
  task_ressult = session.exec(select(Tasks))
  task_with_skill_ressult = session.exec(select(TaskWithSkill))

  assert rol_ressult.first() == saved_rol
  assert user_ressult.first() == saved_user
  assert project_ressult.first() == saved_project
  assert skill_ressult.first() == saved_skill
  assert task_ressult.first() == saved_task
  assert task_with_skill_ressult.first() == saved_task_with_skill
