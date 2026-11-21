from sqlmodel import Session, select, col
from sqlalchemy.orm import joinedload
from .models import ProjectMembers, ProjectMemberCreate
from typing import List
from backend_workpal.database.database import save

class ProjectMemberService:
  def create_project_member(
      self,
      project_id: int,
      new_member_data: ProjectMemberCreate,
      session: Session):
    
      new_project_member = ProjectMembers(
        can_edit_project_details= new_member_data.can_edit_project_details,
        can_manage_tasks= new_member_data.can_manage_tasks,
        can_delete_tasks= new_member_data.can_delete_tasks,
        can_invite_members= new_member_data.can_invite_members,
        is_leader= new_member_data.is_leader,
        id_project= project_id,
        user_id=new_member_data.user_id
      )

      saved_project_member = save(session, new_project_member)

      return saved_project_member