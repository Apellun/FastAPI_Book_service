from typing import Optional
from core.schemas import BaseAPISchemaModel
    
    
class FinishedRead(BaseAPISchemaModel):
    text_id: Optional[int]
    book_id: Optional[int]


class FinishedAdd(BaseAPISchemaModel):
    text_id: int = None
    book_id: int = None
    is_favorite: bool = None