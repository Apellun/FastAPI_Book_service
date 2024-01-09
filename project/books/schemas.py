from datetime import datetime
from typing import List, Dict
from core.schemas import BaseAPISchemaModel, Genre, Author


class BookChapter(BaseAPISchemaModel):
    title: str
    
    
class BookRead(BaseAPISchemaModel):
    id: int
    title: str
    date_created: datetime
    date_updated: datetime = None
    is_completed: bool
    is_public: bool
    authors: List[Author]
    genres: List[Genre]
    parts: List[BookChapter]
    
    
class BookCreate(BaseAPISchemaModel):
    title: str
    is_completed: bool = False
    is_public: bool = False
    parts: Dict[str, int] = None
    genres: List[int] = None
 
    
class BookUpdate(BaseAPISchemaModel):
    title: str = None
    is_completed: bool = False
    is_public: bool = False
    parts: Dict[str, int] = None
    genres: List[int] = None