from fastapi import FastAPI
from src.utils.db import Base, Engine
#from src.tasks.models import TaskModel  # noqa: F401
from src.tasks.router import task_routes  #? use f12 to go for its defintion
from src.user.router import user_routes



Base.metadata.create_all(Engine)

app = FastAPI(title="Task Management App")


'''
#* """ All steps for how to setup backend flow """

|| step 5 || : In {./user/model.py} user model defined done [1] =>
               In {./user/dtos.py} user model ka schema defined means user kya input bhej skta validation [2] => 
               In {./user/controller.py} controller created for registration [3] => 
               In {./user/routes.py} ab mujhe routes banana hai for registration [4] => 
               last In {./main.py} @user_routes ko connect krna hai is main.py file mein [5] | 
'''


app.include_router(task_routes)

#? || STEP:5||
app.include_router(user_routes)







