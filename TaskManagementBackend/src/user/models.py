from src.utils.db import Base
from sqlalchemy import Column , String , Integer , DateTime , Boolean

'''
#*   here , we will define our table schema
'''

class UserModel(Base):
    __tablename__ = "user_table"
    
    id = Column(Integer , primary_key=True)
    name = Column(String)
    username = Column(String , nullable=False)
    hash_password = Column(String , nullable=False)
    email = Column(String)
    
#? STEP 1 table defined ho gya => user model defined ho gya 
#? next step => schema create krna hai schema for this Usermodel 
#? in dtos => where we will define imput / output both 