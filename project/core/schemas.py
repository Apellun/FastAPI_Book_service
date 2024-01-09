from pydantic import BaseModel
from typing import Dict

class BaseAPISchemaModel(BaseModel):
    class Config:
        orm_mode = True
      
        
class Author(BaseAPISchemaModel):
    username: str
    email: str
    

class Genre(BaseAPISchemaModel):
    title: str
        

class NewAuthorsData(BaseAPISchemaModel):
    authors: Dict[str, int]