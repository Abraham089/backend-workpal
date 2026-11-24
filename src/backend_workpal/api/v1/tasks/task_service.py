
from asyncio import Task
from fastapi import HTTPException
from backend_workpal.api.v1.tasks.models import TaskCreate, Tasks, TaskUpdate
from backend_workpal.api.v1.tasks.task_repository import TaskRepository



class TaskService : 
    def __init__(self, repo : TaskRepository):
        self.repo = repo 
        
    def read_all_task(self)-> list[Task]:
        return self.repo.list_all()
    
    def read_task_by_id(self,task_id : int)-> Task|None:
        
        return self.repo.get_by_id(task_id)
        
        
    def read_tasks_by_ids(self, task_ids: list[int]) -> list[Tasks]:
        return self.repo.list_by_ids(task_ids)

    def read_tasks_by_project(self, project_id: int) -> list[Tasks]:
        return self.repo.list_by_project(project_id)

    def create_task(self, data: TaskCreate) -> Tasks:
        return self.repo.save(Tasks.model_validate(data))

    def update_task(self, task_id: int, data: TaskUpdate) -> Tasks | None:
        
        task = self.repo.get_by_id(task_id)
        
        if not task:
            
            return None
        task.sqlmodel_update(data.model_dump(exclude_unset=True))
        return self.repo.save(task)

    def delete_task(self, task_id: int) -> int | None:
        task = self.repo.get_by_id(task_id)
        if not task:
            return None
        self.repo.delete(task)
        return task_id
    
    
    