from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from sqlmodel import Session, select

from backend_workpal.api.v1.project_members.models import ProjectMembers
from backend_workpal.api.v1.users.models import Users
from backend_workpal.database.database import save

from .models import ProjectCreate, Projects, ProjectUpdate


class ProjectService:
  def read_project_by_id(self, project_id:int, session: Session)-> Projects | None:
    statement = select(Projects).where(Projects.id == project_id).options(
      joinedload(Projects.created_by),
      joinedload(Projects.supervisor_user),
    )
    return session.exec(statement).first()

  def read_all_projects(self, session: Session)->list[Projects]:
    statement = select(Projects).options(
      joinedload(Projects.created_by),
      joinedload(Projects.supervisor_user),
    )
    return list(session.exec(statement).all())

  def create_project(self, new_project_data: ProjectCreate,created_id:int,  session: Session):
    if new_project_data.supervisor_user_id is not None and session.get(Users, new_project_data.supervisor_user_id) is None:
      raise HTTPException(
        status_code=404,
        detail=f"No se encontro usuario supervisor con id {new_project_data.supervisor_user_id}",
      )
      
    project = Projects.model_validate(new_project_data, update={"created_by_id": created_id})
    session.add(project)
    
    try:
      session.flush()
      session.add(ProjectMembers(
        user_id=created_id,
        project_id=project.id,
        is_leader=True,
        can_edit_project_details=True,
        can_manage_tasks=True,
        can_delete_tasks=True,
        can_invite_members=True,
      ))
      session.commit()
      
    except IntegrityError:
      
      session.rollback()
      raise HTTPException(status_code=409, detail=f"Ya existe el proyecto {new_project_data.name}") from None

    session.refresh(project)
    return project
      
      
     
    
  
  def update_project(self, updated_project_id: int, updated_project: ProjectUpdate, session: Session):
    updatable_project = self.read_project_by_id(updated_project_id, session)

    if not updatable_project:
      return None

    project_data = updated_project.model_dump(exclude_unset=True)

    if "name" in project_data:
      existe_projecto = session.exec(select(Projects).where(Projects.name == project_data["name"])).first()
      
      
    if existe_projecto and existe_projecto.id != updatable_project :
      raise HTTPException(
        status_code=409,
        detail=f"Ya existe el projecto {project_data['name']}"
      )
      
    if project_data.get('supervisor_user_id') is not None and not session.get(Users, project_data["supervisor_user_id"]):
      
      raise HTTPException(
        status_code= 404,
        detail= f'No se encontro usuario  supervisor con el id {project_data['supervisor_user_id']}'
      )
    
    updatable_project.sqlmodel_update(project_data)

    saved_project = save(session, updatable_project)

    session.refresh(saved_project, ["created_by", "supervisor_user", "members"])

    return saved_project

  def delete_project(self, delete_project_id: int, session: Session):
    delete_project = self.read_project_by_id(delete_project_id, session)

    if not delete_project:
      return None

    session.delete(delete_project)
    session.commit()

    return delete_project_id
  
  def user_can_edit (self,project : Projects,user_id : int, session : Session)-> bool : 
    if project.created_by_id == user_id:
      return True
    
    statement = select(ProjectMembers).where(
      ProjectMembers.project_id == project.id,
      ProjectMembers.user_id == user_id
    )
    member = session.exec(statement).first()
    
    if not member:
      return False

    if member.is_leader or member.can_edit_project_details:
      return True

    return False
  