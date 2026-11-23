from sqlmodel import Session, select, col
from .models import ProjectJoinRequests, ProjectJoinRequestCreate
from ..project_members.service import ProjectMemberService
from backend_workpal.database.database import save

project_member_service = ProjectMemberService()

class JoinRequestService:
  def read_join_request_by_user_and_project_id(self, user_id: int, project_id: int, session: Session):
    statement = select(ProjectJoinRequests).where(
      ProjectJoinRequests.user_id == user_id,
      ProjectJoinRequests.project_id == project_id
      )

    join_request = session.exec(statement).first()

    return join_request

  def create_join_request(
      self,
      user_id: int,
      project_id: int,
      new_join_request_data: ProjectJoinRequestCreate,
      session: Session):
    existing_join_request = self.read_join_request_by_user_and_project_id(user_id, project_id, session)

    existing_member = project_member_service.get_member_project_member_by_project_and_user_ids(
      project_id,
      user_id,
      session
      )

    if existing_join_request or existing_member:
      return None
    
    new_join_request=ProjectJoinRequests.model_validate(new_join_request_data, update={"user_id": user_id, "project_id": project_id})
    saved_join_request = save(session, new_join_request)

    session.refresh(saved_join_request, ["user", "project"])

    return saved_join_request
  