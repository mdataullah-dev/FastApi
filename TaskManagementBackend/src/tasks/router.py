from fastapi import APIRouter, Depends , status
from src.tasks import controller
from src.tasks.dtos import TaskSchema , TaskResponseSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session


task_routes = APIRouter(prefix="/tasks")


#?post
@task_routes.post("/create" , response_model=TaskResponseSchema,  status_code=status.HTTP_201_CREATED)
def create_task(body:TaskSchema, db:Session = Depends(get_db) ):
    return controller.create_task(body, db)

#? dependency injection => ye jo create_task naam ka router hai ye depended hai 
#? ek function pr jsika naam hai [get_db]
#? means jab tak is router/funtion ko hum [get_db] pass nhi karengein tab tak ye properly work nhi karega
#? coz => database provide kr raha hai hume ye get_db


#?get   => fetch all records from database
@task_routes.get("/all_tasks", response_model=List[TaskResponseSchema], status_code= status.HTTP_200_OK)
def get_all_tasks(db:Session = Depends(get_db)):
    return controller.get_tasks(db)


#?get => fetch only a specifc records from a database
@task_routes.get("/one_task/{task_id}", response_model=TaskResponseSchema, status_code= status.HTTP_200_OK)
def get_one_Task(task_id:int , db:Session = Depends(get_db) ):
    return controller.get_oneTask(task_id, db)


#?update => means updating some details for a specific id using put
@task_routes.put("/update_task/{task_id}", response_model=TaskResponseSchema, status_code= status.HTTP_201_CREATED)
def update_task(body:TaskSchema, task_id:int , db:Session = Depends(get_db)):
    return controller.update_task(body , task_id , db)


#?delete => means deleting whole id:
@task_routes.delete("/delete/{task_id}" ,response_model=None, status_code= status.HTTP_204_NO_CONTENT)
def delete(task_id:int, db:Session = Depends(get_db)):
    return controller.delete_task(task_id , db)