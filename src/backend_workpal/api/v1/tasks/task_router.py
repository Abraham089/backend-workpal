from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from starlette import status
from typing import Annotated, List
from backend_workpal.database.database import get_session
from ..users.models import UserResponse
from ..auth.service import get_current_user
from .models import TaskCreate, TaskUpdate, TaskResponse
from .task_repository import TaskRepository
from .task_service import TaskService

router = APIRouter(
  prefix="/tasks",
  tags=["tasks"],
  responses={404: {"description": "not found"}}
)

def get_task_service(session: Annotated[Session, Depends(get_session)]) -> TaskService:
  return TaskService(TaskRepository(session))

CurrentUser = Annotated[UserResponse, Depends(get_current_user)]
Service = Annotated[TaskService, Depends(get_task_service)]


@router.get("/", response_model=List[TaskResponse], status_code=status.HTTP_202_ACCEPTED)
def get_all_tasks(current_user: CurrentUser, service: Service):
  return service.read_all_tasks()

@router.get("/by-ids", response_model=List[TaskResponse], status_code=status.HTTP_202_ACCEPTED)
def get_tasks_by_ids(current_user: CurrentUser, service: Service, ids: Annotated[list[int], Query()]):
  return service.read_tasks_by_ids(ids)


@router.get("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def get_task_by_id(task_id: int, current_user: CurrentUser, service: Service):
  task = service.read_task_by_id(task_id)
  if not task:
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"No se encontro tarea con el id {task_id}")
  return task

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(new_task_data: TaskCreate, current_user: CurrentUser, service: Service):
  return service.create_task(new_task_data)

@router.put("/{task_id}", response_model=TaskResponse, status_code=status.HTTP_202_ACCEPTED)
def put_task(task_id: int, updated_task: TaskUpdate, current_user: CurrentUser, service: Service):
  task = service.update_task(task_id, updated_task)
  if not task:
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"No se encontro tarea con id {task_id} para editar")
  return task

@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, current_user: CurrentUser, service: Service):
  deleted = service.delete_task(task_id)
  if not deleted:
    raise HTTPException(status.HTTP_404_NOT_FOUND, f"No se encontro tarea con id {task_id}")
  return deleted