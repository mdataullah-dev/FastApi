from fastapi import APIRouter, Depends , status
from src.user import controller
from src.user.dtos import userInputSchema , UserResponseSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session


'''
|| step 4 || : user model defined done [1] => user model ka schema defined [2] => controller created for registration [3] => ab mujhe routes banana hai for registration [4] |
|| step 4 || : routes banane ke baad bs mujhe last step [5] is [user_routes] ko connect krna hai main.py file ke sath 
'''



user_routes = APIRouter(prefix="/user")


'''
|| POST ||
'''
@user_routes.post("/register",response_model= UserResponseSchema ,status_code=status.HTTP_201_CREATED)
def userRegister(body:userInputSchema , db:Session = Depends(get_db)):
    return controller.registerUser(body , db )