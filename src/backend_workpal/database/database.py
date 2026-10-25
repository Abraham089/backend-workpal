from sqlmodel import create_engine, SQLModel, Session
from src.backend_workpal.api.v1.task_with_skill.models import TaskWithSkill
from src.backend_workpal.api.v1.tasks.models import Tasks
from src.backend_workpal.api.v1.skills.models import Skills
from src.backend_workpal.api.v1.users.models import Users
from src.backend_workpal.api.v1.projects.models import Projects
from src.backend_workpal.api.v1.roles.models import Roles

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()

def get_session():
    with Session(engine) as session:
        yield session

def save(session: Session, model_instance):
    session.add(model_instance)
    session.commit()
    session.refresh(model_instance)
    return model_instance