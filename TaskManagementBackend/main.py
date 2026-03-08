from fastapi import FastAPI
from src.utils.db import Base, Engine
#from src.tasks.models import TaskModel  # noqa: F401
from src.tasks.router import task_routes  #? use f12 to go for its defintion

Base.metadata.create_all(Engine)

app = FastAPI(title="Task Management App")

app.include_router(task_routes)




