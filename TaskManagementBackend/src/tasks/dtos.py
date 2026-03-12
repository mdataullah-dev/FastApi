from pydantic import BaseModel

class TaskSchema(BaseModel):
    title : str
    description : str 
    is_completed : bool = False
    
    
class TaskResponseSchema(BaseModel):
    id: int
    title : str
    description : str 
    is_completed : bool 
    
    user_id : int | None = 0  #? added after alembic migration of user_id into task table
    