


from sqlmodel import Session, col, select

from backend_workpal.api.v1.tasks.models import Tasks
from backend_workpal.database.database import save


class TaskRepository : 
    def __init__(self, db : Session):
        self.db = db
        
    def list_all(self)-> list[Tasks]:
        return list(self.db.exec(select(Tasks)).all())
    
    def get_by_id(self,task_id: int)->Tasks| None:
        return self.db.get(Tasks,task_id)
    
    def get_by_ids(self,task_id : list[int])->list[Tasks]:
        if not task_id : 
            return []
        
        return list(self.db.exec(select(Tasks).where(col(Tasks.id).in_(task_id))).all())
    
    def list_by_project(self,project_id : int)-> list[Tasks]:
        return list(self.db.exec(select(Tasks).where(Tasks.project_id == project_id)).all())
    
    def save(self,task : Tasks)-> Tasks:
        return save(self.db,task)
    
    def delete ( self,task : Tasks)->None: 
        self.db.delete(task)
        self.db.commit()
        
        