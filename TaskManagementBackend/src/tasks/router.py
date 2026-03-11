from fastapi import APIRouter, Depends , status
from src.tasks import controller
from src.tasks.dtos import TaskSchema , TaskResponseSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session


#* DEPENDENCY THAT WE MADE
from src.utils.helpers import is_authenticated
from src.user.models import UserModel


task_routes = APIRouter(prefix="/tasks")


'''
|| POST ||
'''
@task_routes.post("/create" , response_model=TaskResponseSchema,  status_code=status.HTTP_201_CREATED)
def create_task(body:TaskSchema, db:Session = Depends(get_db) , user:UserModel = Depends(is_authenticated)):     #* if is_authenticated successfully kaam krega tabhi hamara system/royte controller ko return krega => 
    return controller.create_task(body, db)                                                                      #*  user:UserModel = Depends(is_authenticated)  => is_authenticated return karega [user] => jo is yahan wale user varaible mein store ho jayega and => is user:UserModel type UserModel isliye hai kyu ki user : userModel class ka hi ek object hai


'''
=>  here , kya hoga is depedency ki wajah se => checking our post route | create route protected hua ya nhi hua 

in postman : on create task api => when we will hit api => we get unauthorized error

bacause => humne system pr pehle || #*LOGIN || krna hai then uske baad is create_task wali api ke || header || mein authrorization key and token send krna hai 

'''  

#? dependency injection => ye jo create_task naam ka router hai ye depended hai 
#? ek function pr jsika naam hai [get_db]
#? means jab tak is router/funtion ko hum [get_db] pass nhi karengein tab tak ye properly work nhi karega
#? coz => database provide kr raha hai hume ye get_db


'''
|| GET || : fetch all records from database ||
'''
@task_routes.get("/all_tasks", response_model=List[TaskResponseSchema], status_code= status.HTTP_200_OK)
def get_all_tasks(db:Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_tasks(db)


'''
|| GET || : fetch only a specifc records from a database ||
'''
@task_routes.get("/one_task/{task_id}", response_model=TaskResponseSchema, status_code= status.HTTP_200_OK)
def get_one_Task(task_id:int , db:Session = Depends(get_db), user:UserModel = Depends(is_authenticated) ):
    return controller.get_oneTask(task_id, db)


'''
|| update || : means updating some details for a specific id using put ||
'''
@task_routes.put("/update_task/{task_id}", response_model=TaskResponseSchema, status_code= status.HTTP_201_CREATED)
def update_task(body:TaskSchema, task_id:int , db:Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.update_task(body , task_id , db)

'''
|| DELETE || : means deleting whole id ||
'''
@task_routes.delete("/delete/{task_id}" ,response_model=None, status_code= status.HTTP_204_NO_CONTENT)
def delete(task_id:int, db:Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.delete_task(task_id , db)



#? || USER login krne ke baad => usko jo token milega => usko pass karega => sare CRUD operations perform krne ke liye in tasks API in header in postman as "authorization":"token" => then sahi hoga toh access milega 