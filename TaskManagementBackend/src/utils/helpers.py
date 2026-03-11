from fastapi import Request , status , HTTPException , Depends
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError , ExpiredSignatureError
from src.user.models import UserModel
from src.utils.settings import settings


from src.utils.db import get_db


'''
|| SAME AS is_authenticated controller =>  just 2 changes yahan pr v depends lagega for get_db ||

|| NOW bs is_authenticated act as dependency isko router mein connnect krna hai ||

|| we will connect this into => ./src/task/router.py => wahan pr user CRUD krne se pehle authenticate hai ki nhi is dependency se pata lagega
'''

def is_authenticated(request:Request , db:Session = Depends(get_db)):
   
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no Token")
       
        token = token.split(" ")[-1]
        
        data = jwt.decode(token , settings.SECRET_KEY , settings.ALGORITHM)
        
        user_id = data.get("_id")
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="User doesn't exist || you are unauthorized")

        return user   
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
       
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
