from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel

##!POST
def create_task(body:TaskSchema , db:Session):
    
    #print(body.model_dump())
    data = body.model_dump()
    
    new_task = TaskModel(
        title = data["title"],
        description = data["description"],
        is_completed = data["is_completed"]
    )                        #? TaskModel class ki ek object bani hai jisko humne new_task mein store kr dia hai 
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    return {
        "status": 200,
        "msg" : "Task Created Successfully",
        "data": new_task
    }


##! GET endpoint

def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    return {
        "status": 200,
        "msg" : "Task Retreived Successfully",
        "data": tasks
    }
