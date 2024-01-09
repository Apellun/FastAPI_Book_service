from sqlalchemy import (
    Column, Integer, String
)
from sqlalchemy.orm import relationship
from core.db import Base
    
        
class Genre(Base):
    __tablename__ = "genre"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    
    text_genres = relationship('Text', secondary='text_genre', back_populates='genres', lazy="joined")
    book_genres = relationship('Book', secondary='book_genre', back_populates='genres', lazy="joined")
    

class Role(Base):
    __tablename__ = "role"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)