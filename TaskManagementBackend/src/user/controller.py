from src.user.dtos import userInputSchema , loginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException , status
from pwdlib import PasswordHash # type: ignore
import jwt # type: ignore
from src.utils.settings import settings
from datetime import datetime , timedelta


'''
|| step 3 || : user model defined => user model ka schema defined => ab mujhe controller create krna hai |

| OAuth2 with password & hashing , Bearer with JWT tokens |

| bearer => Jo person token ko hold karta hai (bearer), usko access milta hai. |
'''

#? ek object bana liya i.e password_hash
password_hash = PasswordHash.recommended()

def get_password_hash(password):
    return password_hash.hash(password)   #? ye return karega hash password

def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)

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

'''
|| LOGIN OF USER ||
'''

def login_user(body:loginSchema , db:Session): 
    #? yahan pr body mein 2 cheez chaiye username  &  password
    #? ab is body ka type define krna padega => inside dtos.py mein jayengein 
    
    #print(body)  #? it means humne jo v data hamare endpoint pr se send kiya postman se kya hamare backend pr recieve hua => toh yes hua recieve 
    #* now mujhe backend pr data receive ho raha hai 
    #* ab mujhe sabse pehle check krna hai kya username sahi hai 
    #* if username sahi hai then kya ye username jis user ka uska password b match krta hai
    #* if YES , then we proceeds only 
    
    user = db.query(UserModel).filter(UserModel.username == body.username).first()    #? yahan pr UserModel.username means table mein jo username hai already and || jo body.username => user ne bheja dono equal hain ki nhi 
    if not user:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="You Entered Wrong username")
    
    #if user.hash_password == body.password  #* ye hum nhi kr skte kyu ki user jo ne bheja hoga body mein vo actual password ...=> user.hashpassword jo user ke database meim store kiya hua hai 
    #? decryption krna padega 
    
    if not verify_password( body.password , user.hash_password):     #? verify hua toh true || else false dega ye function
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="You Entered Wrong password")
 
    #? if dono uper wali condition false ho gyi then user sahi hai then we will generate token 
    
    exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME) # current time mein + 30 minutes uske baad expire ho jayega 
    
    token = jwt.encode({"_id":user.id , "exp":exp_time} , settings.SECRET_KEY , settings.ALGORITHM)
    print(exp_time)
    
    
    '''
        ye jwt.encode() mein hum 3 cheez pass krte hain => payload , secret key , algorithm
        
        PAYLOAD means => kis data ke behalf pr hum token generate krna chahte hain
        SECRET KEY => responsible for encoding and decoding our token
        ALGORITHM => use krega SECRET KEY => and then apne {PAYLOAD} ko endcode kr ke ek JWT token genrate krna chahte hain
        
        {payload} -> mein hum store krte hain unique values => toh kisi v ek ya ek se jaydah unique vlaues ko database se hum payload mein daal kr encode kr ke usse token neikaal skte 
        
        #* token same user ke liye v har baar different mile uske liye we use [expiry time]
        
        timedelta =>  to add some time i.e minutes
    '''
    return {
        "token" : token   #? token bhejna cumpulsory hai 
    }