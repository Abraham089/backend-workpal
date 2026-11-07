from sqlmodel import Session, select

from backend_workpal.database.database import save
from backend_workpal.api.v1.task_with_skill.models import TaskWithSkill
from backend_workpal.api.v1.tasks.models import Tasks
from backend_workpal.api.v1.skills.models import Skills
from backend_workpal.api.v1.users.models import Users
from backend_workpal.api.v1.projects.models import Projects
from backend_workpal.api.v1.roles.models import Roles
from backend_workpal.api.v1.project_members.models import ProjectMembers

def test_create_things_in_db(session: Session):
  rol = Roles(name= "admin")
  saved_rol = save(session, rol)

  user = Users(
    name="example name",
    last_name="example last name",
    username="example123",
    mail="examplemail@gmail.com",
    password_hash= "example123",
    is_active=True,
    role_id= 1)
  saved_user = save(session, user)

  project = Projects(
    name= "Example Project",
    description= "Example description",
    img= "img example",
    created_by_id= saved_user.id)
  saved_project = save(session, project)

  project_member = ProjectMembers(
    can_delete_tasks=True,
    can_invite_members=True,
    can_edit_project_details=True,
    is_leader=True,
    user_id=saved_user.id,
    project_id=saved_project.id
  )
  saved_project_member = save(session, project_member)

  skill = Skills(name="Example skill")
  saved_skill = save(session, skill)

  task = Tasks(
    name= "Example Task",
    description= "Example description",
    status= "Ok",
    project_id= saved_project.id,
    user_id= saved_user.id)
  saved_task = save(session, task)

  task_with_skill = TaskWithSkill(task_id=1, skill_id=1)
  saved_task_with_skill = save(session, task_with_skill)

  rol_ressult = session.exec(select(Roles))
  user_ressult = session.exec(select(Users))
  project_ressult = session.exec(select(Projects))
  skill_ressult = session.exec(select(Skills))
  task_ressult = session.exec(select(Tasks))
  task_with_skill_ressult = session.exec(select(TaskWithSkill))
  project_member_ressult = session.exec(select(ProjectMembers))

  assert rol_ressult.first() is not None
  assert user_ressult.first() is not None
  assert project_ressult.first() is not None
  assert skill_ressult.first() is not None
  assert task_ressult.first() is not None
  assert task_with_skill_ressult.first() is not None
  assert project_member_ressult.first() is not None
