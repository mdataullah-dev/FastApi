from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException

##!POST
def create_task(body:TaskSchema , db:Session):
    
    #print(body.model_dump())
    data = body.model_dump()
    
    #? new object bana rahe of our task model 
    new_task = TaskModel(
        title = data["title"],
        description = data["description"],
        is_completed = data["is_completed"]
    )                        #? TaskModel class ki ek object bani hai jisko humne new_task mein store kr dia hai 
    
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    
    # return {
    #     "status": 200,
    #     "msg" : "Task Created Successfully",
    #     "data": new_task
    # }
    return new_task


##! GET endpoint

#?get   => fetch all records from database
def get_tasks(db:Session):
    tasks = db.query(TaskModel).all()
    # return {
    #     "status": 200,
    #     "msg" : "Task Retreived Successfully",
    #     "data": tasks
    # }
    return tasks
    
    
#?get => fetch only a specifc records from a database
def get_oneTask(task_id:int, db:Session):
    
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail="Task Id not found")
    # 
    return one_task
    
    
#?update => already created task ko update kaise krna hai 
def update_task(body:TaskSchema, task_id:int , db:Session):
    
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail="Task Id not found")
    
    # one_task.title = body.title
    # one_task.description = body.description
    # one_task.is_completed = body.is_completed
    #* ye one by one krna is long process
    
    body = body.model_dump()        #? converted into dict
    for key,value in body.items():  #? by .items => we get key value pairs
        setattr(one_task , key , value)
    
    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    
    # 
    return one_task


#? delete => delete the task from database
def delete_task(task_id:int, db:Session):
    
    one_task = db.query(TaskModel).get(task_id)
    if not one_task:
        raise HTTPException(404, detail="Task Id not found")
    
    db.delete(one_task)
    db.commit()
    
    # return{
    #     "status": 200,
    #     "msg" : "Task Deleted Successfully",
    #     "data": task_id
    # }
    #? delete ka controller kuch v return nhi krta :
    return None
    
#? for get we use 200
#? for post and put we use 201
#? for delete we return None from controller
#? 204 for no content  => for delete we use this => use in router

#* in router for all these endpoint fastapi provides status that is being used in router.py
#? hamesha hum apne router mein dete hain status code
