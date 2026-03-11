from pydantic import BaseModel

#? ||step 2||  :  | userModel ka schema banega yahan pr ki hum kya input le skte and kya ouput dengein |

#* just like we did for taskModel in ./task/dtos.py

class userInputSchema(BaseModel):
    name : str
    username : str
    #hash_password : str        *** hash_password nhi hoga => #? kyu ki user toh password hi bhejega hum backend mein use chnage krengein krengein | encrypt krengein and store krengein hash password naam ki feild ke ander 
    password : str
    email : str
    
    
#* RESPONSE Schema hanta kr run kro hashpassword ayega in our postman if call register api
class UserResponseSchema(BaseModel):   #?hash password hum show nhi karengein in response 
    name : str 
    username : str
    email : str
    id : int 

#? next step 3 => controller defined krna hai 
    
   
#* for ||login|| defining body type   
class loginSchema(BaseModel):
    username : str
    password : str 