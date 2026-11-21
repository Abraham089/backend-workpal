from sqlmodel import Session, select, col
from sqlalchemy.orm import joinedload
from .models import Projects, ProjectCreate, ProjectUpdate
from ..project_members.models import ProjectMemberCreate
from ..project_members.service import ProjectMemberService
from typing import List
from backend_workpal.database.database import save

project_member_service = ProjectMemberService()

class ProjectService:
  def read_project_by_id(self, project_id:int, session: Session):
    statement = select(Projects).where(Projects.id == project_id).options(
      joinedload(Projects.created_by),
      joinedload(Projects.supervisor_user),
      joinedload(Projects.members)
      )
    project = session.exec(statement).first()
    
    return project

  def read_all_projects(self, session: Session):
    projects = select(Projects).options(
      joinedload(Projects.created_by),
      joinedload(Projects.supervisor_user),
      joinedload(Projects.members)
      )
    return session.exec(projects).all()

  def create_project(self, new_project_data: ProjectCreate, session: Session):
    new_project = Projects(
      name=new_project_data.name,
      description=new_project_data.description,
      img=new_project_data.img,
      created_at=new_project_data.created_at,
      status=new_project_data.status,
      ending_date=new_project_data.ending_date,
      created_by_id=new_project_data.created_by_id,
      supervisor_user_id=new_project_data.supervisor_user_id
    )

    session.add(new_project)

    new_member_data = ProjectMemberCreate(
      can_edit_project_details= True,
      can_manage_tasks= True,
      can_delete_tasks= True,
      can_invite_members= True,
      is_leader= True,
      user_id=new_project_data.created_by_id
      )
    
    new_member = project_member_service.create_project_member(new_project.id, new_member_data, session)
    
    if not new_member:
      session.rollback()
      return None

    session.commit()
    session.refresh(new_member)

    return new_project

  def update_project(self, updated_project_id: int, updated_project: ProjectUpdate, session: Session):
    updatable_project = self.read_project_by_id(updated_project_id, session)

    if not updatable_project:
      return None

    project_data = updated_project.model_dump(exclude_unset=True)

    updatable_project.sqlmodel_update(project_data)

    saved_project = save(session, updatable_project)

    session.refresh(saved_project, ["created_by", "supervisor_user"])

    return saved_project

  def delete_project(self, delete_project_id: int, session: Session):
    delete_project = self.read_project_by_id(delete_project_id, session)

    if not delete_project_id:
      return None

    session.delete(delete_project)
    session.commit()

    return delete_project_id
  