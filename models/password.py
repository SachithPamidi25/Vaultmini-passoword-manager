from pydantic import BaseModel

class StorePassword(BaseModel):
    service:str        
    username:str       
    password:str       
 