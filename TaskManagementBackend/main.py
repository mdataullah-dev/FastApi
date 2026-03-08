from fastapi import FastAPI
from src.utils.db import Base, Engine
from src.tasks.models import TaskModel

Base.metadata.create_all(Engine)

app = FastAPI(title="Task Management App")




