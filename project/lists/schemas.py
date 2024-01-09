from typing import Optional
from core.schemas import BaseAPISchemaModel

class Book(BaseAPISchemaModel):
    title: str
    

class Text(BaseAPISchemaModel):
    title: str
    
    
class ListRead(BaseAPISchemaModel):
    text_id: Optional[int]
    book_id: Optional[int]
    
    
class BookmarksRead(BaseAPISchemaModel):
    text_id: Book
    book_id: Text
    

class FinishedAdd(BaseAPISchemaModel):
    text_id: int = None
    book_id: int = None
    is_favorite: bool = None
    
    
class BookmarkCreate(BaseAPISchemaModel):
    text_id: Book
    book_id: Text
    
class ReadlistCreate(BaseAPISchemaModel):
    text_id: Book = None
    book_id: Text = None