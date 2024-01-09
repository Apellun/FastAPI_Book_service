from datetime import datetime
from typing import List
from core.schemas import BaseAPISchemaModel, Author, Genre


class TextBook(BaseAPISchemaModel):
    title: str
    
    
class TextRead(BaseAPISchemaModel):
    id: int
    title: str
    date_created: datetime
    date_updated: datetime = None
    content: str
    is_public: bool
    is_singular: bool
    creators: List[Author]
    genres: List[Genre]
    books: List[TextBook]
    
    
class TextCreate(BaseAPISchemaModel):
    title: str
    content: str
    genres: List[int] = None
    is_public: bool = False
    is_singular: bool = True
 
    
class TextUpdate(BaseAPISchemaModel):
    title: str = None
    content: str = None
    is_public: bool = None
    is_singular: bool = None
    genres: List[int] = None