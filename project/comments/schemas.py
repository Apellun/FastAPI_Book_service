from datetime import datetime
from core.schemas import BaseAPISchemaModel, Author
    
    
class CommentRead(BaseAPISchemaModel):
    id: int
    author: int #TODO: find a way to attach a User instance
    content: str
    date_posted: datetime
    was_updated: bool
    
    
class CommentCreateUpdate(BaseAPISchemaModel):
    content: str