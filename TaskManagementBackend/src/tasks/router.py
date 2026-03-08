from fastapi import APIRouter, Depends
from src.tasks import controller
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db


task_routes = APIRouter(prefix="/tasks")
#?post
@task_routes.post("/create")
def create_task(body:TaskSchema, db = Depends(get_db) ):
    return controller.create_task(body, db)

#? dependency injection => ye jo create_task naam ka router hai ye depended hai 
#? ek function pr jsika naam hai [get_db]
#? means jab tak is router/funtion ko hum [get_db] pass nhi karengein tab tak ye properly work nhi karega
#? coz => database provide kr raha hai hume ye get_db


#?get
@task_routes.get("/all_tasks")
def get_all_tasks(db = Depends(get_db)):
    return controller.get_tasks(db)
