from sqlmodel import create_engine, SQLModel, Session
from backend_workpal.api.v1.task_with_skill.models import TaskWithSkill
from backend_workpal.api.v1.tasks.models import Tasks
from backend_workpal.api.v1.skills.models import Skills
from backend_workpal.api.v1.roles.models import Roles
from backend_workpal.api.v1.comments.models import Comments
from backend_workpal.api.v1.institutions.models import Institutions
from backend_workpal.api.v1.institution_with_user.models import InstitutionWithUser
from backend_workpal.api.v1.users.models import Users, UserResponse, UserSummary
from backend_workpal.api.v1.projects.models import Projects, ProjectResponse, ProjectSummary
from backend_workpal.api.v1.project_members.models import ProjectMembers, ProjectMemberResponse

ProjectMemberResponse.model_rebuild()
UserResponse.model_rebuild()
ProjectResponse.model_rebuild()

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