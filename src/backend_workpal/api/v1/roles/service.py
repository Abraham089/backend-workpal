from sqlmodel import Session, select
from .models import Roles, RoleCreate
from backend_workpal.database.database import save

class RoleService:
  def read_role_by_id(self, role_id:int, session: Session):
    statement = select(Roles).where(Roles.id == role_id)
    role = session.exec(statement).first()
      
    return role

  def read_all_roles(self, session: Session):
    roles = select(Roles)
    return session.exec(roles).all()

  def create_role(self, new_role_data: RoleCreate, session:Session):
    new_role = Roles(
      name=new_role_data.name
    )
    saved_role = save(session, new_role)
    return saved_role
