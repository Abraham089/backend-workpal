from fastapi import HTTPException,status
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError
from backend_workpal.api.v1.users.models import Users
from .models import ProjectMembers, ProjectMemberCreate, ProjectMemberUpdate
from backend_workpal.database.database import save # type: ignore
from .models import ProjectMemberCreate,ProjectMemberUpdate,ProjectMembers

PERMISOS = ("can_edit_project_details", 
            "can_manage_tasks", 
            "can_delete_tasks", 
            "can_invite_members")

class ProjectMemberService:
  def get_project_members_by_project_id(
    self,
    project_id: int,
    session: Session
    ):

    statement = select(ProjectMembers).options(
      joinedload(ProjectMembers.user),
      joinedload(ProjectMembers.project)
    ).where(ProjectMembers.project_id == project_id)

    project_members = session.exec(statement).unique().all()
      
    return project_members
  
  def get_project_member_by_project_and_user_ids(
    self,
    project_id: int,
    member_id: int,
    session: Session
    ):

    existing_member = session.exec(
      select(ProjectMembers).options(
        joinedload(ProjectMembers.user),
        joinedload(ProjectMembers.project)
      ).where(
        ProjectMembers.project_id == project_id,
        ProjectMembers.user_id == member_id,
        )
      ).first()
    
    return existing_member


  def build_member(
    self,
    project_id: int,
    new_member_data: ProjectMemberCreate,
    session: Session,
    invitador : ProjectMembers | None = None
    )-> ProjectMembers:
    
    if session.get(Users,new_member_data.user_id) is None : 
      raise HTTPException (
        status_code= status.HTTP_404_NOT_FOUND,
        detail= f"no se encontro usuario con id {new_member_data.user_id}"
        )
      
    if invitador is not None and not invitador.is_leader : 
      pordefecto = ProjectMemberCreate(user_id = new_member_data.user_id )
      if any(getattr(new_member_data,permisos) != getattr(pordefecto, permisos ) for permisos in PERMISOS):
        raise HTTPException(
          status.HTTP_403_FORBIDDEN,
          detail="Solo el lider del proyecto puede asignar permisos al invitar",
        )
        
    return ProjectMembers(project_id=project_id, is_leader=False, **new_member_data.model_dump()) 


  def create_project_member(
    self,
    project_id: int,
    new_member_data: ProjectMemberCreate,
    session: Session,
    invitador : ProjectMembers | None = None
    ):
    
    existing_member = self.build_member(project_id, new_member_data, session, invitador)
    
    try:
      return save(session,existing_member)
    except IntegrityError : 
        session.rollback()
        
        return None

    
    # existing_member = self.get_project_member_by_project_and_user_ids(project_id, new_member_data.user_id, session)

    # if existing_member:
    #   return None
    
    # new_project_member = ProjectMembers(
    #   can_edit_project_details= new_member_data.can_edit_project_details,
    #   can_manage_tasks= new_member_data.can_manage_tasks,
    #   can_delete_tasks= new_member_data.can_delete_tasks,
    #   can_invite_members= new_member_data.can_invite_members,
    #   is_leader= new_member_data.is_leader,
    #   project_id= project_id,
    #   user_id=new_member_data.user_id
    # )

    # saved_project_member = save(session, new_project_member)

    # return saved_project_member

  def update_project_member(
      self,
      update_data: ProjectMemberUpdate,
      updatable_member: ProjectMembers,
      session: Session
      ):
    
    update_member_data = update_data.model_dump(exclude_unset=True)

    updatable_member.sqlmodel_update(update_member_data)

    saved_member = save(session, updatable_member)

    session.refresh(saved_member, ["user", "project"])

    return saved_member
  