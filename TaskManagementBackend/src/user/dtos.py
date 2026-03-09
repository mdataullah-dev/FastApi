from pydantic import BaseModel

#? ||step 2||  :  | userModel ka schema banega yahan pr ki hum kya input le skte and kya ouput dengein |

#* just like we did for taskModel in ./task/dtos.py

class userInputSchema(BaseModel):
    name : str
    username : str
    #hash_password : str        *** hash_password nhi hoga => #? kyu ki user toh password hi bhejega hum backend mein use chnage krengein krengein | encrypt krengein and store krengein hash password naam ki feild ke ander 
    password : str
    email : str
    
    

#class UserResponseSchema(BaseModel):



#? next step 3 => controller defined krna hai 
    
     
    