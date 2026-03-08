from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".venv", extra="ignore")
    
    DB_CONNECTION:str
    
    
settings = Settings()   #? settings naam ki object bn gyi hai ==> jisme Settings class ki sari properties hain 

#? ever we need database => then just we import settings and do => settings.db_connection

print(settings.DB_CONNECTION)  #* jab v server start hoga db connection terminal pr print hoga 