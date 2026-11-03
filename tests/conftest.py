import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from backend_workpal.main import app
from backend_workpal.database.database import get_session

from backend_workpal.api.v1.task_with_skill.models import TaskWithSkill
from backend_workpal.api.v1.tasks.models import Tasks
from backend_workpal.api.v1.skills.models import Skills
from backend_workpal.api.v1.users.models import Users
from backend_workpal.api.v1.projects.models import Projects
from backend_workpal.api.v1.roles.models import Roles

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
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(name="client")  
def client_fixture(session: Session):  
    def get_session_override():  
        return session

    app.dependency_overrides[get_session] = get_session_override  

    client = TestClient(app)  
    yield client  
    app.dependency_overrides.clear()