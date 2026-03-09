from src.user.dtos import userInputSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException


'''
|| step 3 || : user model defined => user model ka schema defined => ab mujhe controller create krna hai |

| OAuth2 with password & hashing , Bearer with JWT tokens |

| bearer => Jo person token ko hold karta hai (bearer), usko access milta hai. |
'''


def registerUser(body:userInputSchema, db:Session):    #? isme do cheez cumpulsory ayega => user ka data jo hum body mein lengein and dtos se validate krengein  and database
    #? user ka data => uska type hai userinputSchema and database db : uska type hai Session
    print(body)
    return {
        "msg" : "Registration Done"     
    }                                   #* jaise hi controller define ho gya bn gya we will go into router.py and create routes 