from src.user.dtos import userInputSchema , loginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from fastapi import HTTPException , status , Request
from pwdlib import PasswordHash # type: ignore
import jwt # type: ignore
from src.utils.settings import settings
from datetime import datetime , timedelta
from jwt import ExpiredSignatureError, InvalidTokenError


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
    
    #exp_time = datetime.now() + timedelta(minutes=settings.EXP_TIME) # current time mein + 30 minutes uske baad expire ho jayega 
    exp_time = datetime.now() + timedelta(seconds=55)
    
    token = jwt.encode({"_id":user.id , "exp":exp_time.timestamp()} , settings.SECRET_KEY , settings.ALGORITHM)
    #print(exp_time)
    
    
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
    
    
    
'''
#! BASED on the token : [[how to authenticate the user]]

till now : we learn user login : if user put correct username and password then hum means backend usko validate kr ke ek correct token generate kr ke dengein

but today : based on that token => jo user ne during login generate kiya hai -> hum user ko authenticate kaise kr skte hain? ki vo kis user ka token? and and uski kya details hain?

#? steps to validate the token:

   1. jab v koi user api call karega sath mein token send karega --> in request body mein send karega => headers ki form mein bhejegein ye token (user bhejega)
   2. is [header] ko apne backend mein read / nikalengein kaise
   3. then is [header] ko validate kr lengein
   4. then data ko fetch kr ke 
   5. then user ko return mein response bhej dengein
   
'''
def is_authenticated(request:Request , db:Session):
    # request har endpoint ke sath attach hoti just mujhe usse nikalna aana chaiye
    
    #print(request.headers)  #? request ek object hai 
    '''
    Headers({
        'authorization': 'jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOjMsImV4cCI6MTc3MzIzNzYzNn0.AdXAz9a1sll1fl2FCIxNP54DHifQQ7LpsPriwYN0Zoo',
        'content-type': 'text/plain',
        'user-agent': 'PostmanRuntime/7.52.0',
        'accept': '*/*',
        'postman-token': '881d656d-8392-4e54-b0f2-9a59e2837040',
        'host': '127.0.0.1:8000',
        'accept-encoding': 'gzip, deflate, br',
        'connection': 'keep-alive', 'content-length': '10'
    })
    
    headers ek dict hai uske ander ke key hai authorization
    '''
    try:
        token = request.headers.get("authorization")
        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="no Token")
        #print(token) 
        token = token.split(" ")[-1]
        
        data = jwt.decode(token , settings.SECRET_KEY , settings.ALGORITHM)
        
        #print(data)   #? {'_id': 3, 'exp': 1773239661} => jis user ne login kiya tha uski id mil rahi 
        
        user_id = data.get("_id")
        # expiry_time = int(data.get("exp"))
        # #print(expiry_time)
        
        # current_time = datetime.now().timestamp()
        # #print(current_time)
        
        # print(expiry_time - current_time)
        # if current_time > expiry_time:
        #     raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="TimeOut || you are unauthorized") 
        
        user = db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED , detail="User doesn't exist || you are unauthorized")
 
        #? ye user wala tab run hoga jab => database mein alreay register tha id:4 ya koi v id => id:4 ne login mara => then id:4 database se delete kr diya humne => then id:4 ke liye jo login ke time token mila tha usko header mein daal kr authentication krne gye and => then hame milega ye wala user wala exception
        # return {
        #     "msg" : "Done"
        # }
        return user    #? user ki details ajayegi sari aise return krne se
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
       
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


'''
|| GET : ALL USERS DETAILS ||
'''
def get_users(db:Session):
    users = db.query(UserModel).all()
    return users

#----------------------------------------------------------------------------------------------

'''
|| DELETE : DELETE A SINGLE USER FROM DATABASE ||
'''
def delete_user(user_id:int, db:Session):
    one_user = db.query(UserModel).get(user_id)
    if not one_user:
        raise HTTPException(404, detail="Task Id not found")
    
    db.delete(one_user)
    db.commit()
    return None

#--------------------------------------------------------------------------------------------------------