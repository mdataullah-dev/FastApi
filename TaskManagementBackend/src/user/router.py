from fastapi import APIRouter, Depends , status , Request
from src.user import controller
from src.user.dtos import userInputSchema , UserResponseSchema , loginSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session


'''
|| step 4 || : user model defined done [1] => user model ka schema defined [2] => controller created for registration [3] => ab mujhe routes banana hai for registration [4] |
|| step 4 || : routes banane ke baad bs mujhe last step [5] is [user_routes] ko connect krna hai main.py file ke sath 
'''



user_routes = APIRouter(prefix="/user")


'''
|| POST : REGISTRATION ||
'''
@user_routes.post("/register",response_model= UserResponseSchema ,status_code=status.HTTP_201_CREATED)
def userRegister(body:userInputSchema , db:Session = Depends(get_db)):
    return controller.registerUser(body , db )

'''
|| POST : LOGIN ||
'''
@user_routes.post("/login", status_code=status.HTTP_200_OK)   #? yahan pr 200 hi rakha kyu ki database mein kuch create nhi kr rahein hain hum 
def login(body:loginSchema , db:Session = Depends(get_db)):
    return controller.login_user(body , db)

'''
|| GET : IS_AUTHENTICATED ||
'''
@user_routes.get("/is_auth" ,response_model=UserResponseSchema , status_code=status.HTTP_200_OK)
def is_auth(request:Request , db:Session = Depends(get_db)):
    return controller.is_authenticated(request , db )


'''
|| GET : ALL USERS DETAILS ||
'''
@user_routes.get("/all_users", response_model=List[UserResponseSchema], status_code= status.HTTP_200_OK)
def get_all_users(db:Session = Depends(get_db)):
    return controller.get_users(db)


'''
|| DELETE : DELETE A SINGLE USER FROM DATABASE || 
'''
@user_routes.delete("/delete/{user_id}" ,response_model=None, status_code= status.HTTP_204_NO_CONTENT)
def delete(user_id:int, db:Session = Depends(get_db)):
    return controller.delete_user(user_id , db)

'''
|| GET || : A SINGLE USER DETAILS ||
'''
@user_routes.get("/one_user/{user_id}", response_model=UserResponseSchema, status_code= status.HTTP_200_OK)
def get_one_user(user_id:int , db:Session = Depends(get_db) ):
    return controller.get_oneUser(user_id, db)
