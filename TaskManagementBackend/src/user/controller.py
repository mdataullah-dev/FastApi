from src.user.dtos import userInputSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException
from pwdlib import PasswordHash # type: ignore


'''
|| step 3 || : user model defined => user model ka schema defined => ab mujhe controller create krna hai |

| OAuth2 with password & hashing , Bearer with JWT tokens |

| bearer => Jo person token ko hold karta hai (bearer), usko access milta hai. |
'''

#? ek object bana liya i.e password_hash
password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)   #? ye return karega hash password

#---------------------------------------------------------------------------------------------------------------------------------------------------------
'''
||  POST : REGISTER USER TO THE DATABASE||
'''
def registerUser(body:userInputSchema, db:Session):    #* isme do cheez cumpulsory ayega => user ka data jo hum body mein lengein and dtos se validate krengein  and database
    #? user ka data => uska type hai userinputSchema and database db : uska type hai Session
    #print(body)
    ## username validation => duplicate toh nhi hai
    ## email validation    => unique honi chaiye 
    
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()    #? yahan pr UserModel.username means table mein jo username hai already and || jo body.username => user ne bheja dono equal hain ki nhi 
    if is_user:
        raise HTTPException(400 , detail="Username already exists...")
    
    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        raise HTTPException(400 , detail="Email address already exists...")
    
    
    #! if dono false hoti hai then || we will do hashing ||
    
    hash_password = get_password_hash(body.password)
    
    #? last step : Creating the object of our user model
    new_user = UserModel(
        name = body.name,
        username = body.username,
        hash_password = hash_password,
        email = body.email   
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user                               #* jaise hi controller define ho gya bn gya we will go into router.py and create routes 
#-------------------------------------------------------------------------------------------------------------