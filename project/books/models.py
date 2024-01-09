from datetime import datetime
from sqlalchemy import (
    Boolean, Column, Integer,
    String, DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from core.db import Base
from core.models import Role, Genre

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    date_updated = Column(DateTime)
    is_completed = Column(Boolean)
    is_public = Column(Boolean)
    
    authors = relationship('User', secondary='book_author', back_populates='books', lazy="joined")
    parts = relationship('Text', secondary='book_part', back_populates='books', lazy="joined")
    genres = relationship('Genre', secondary='book_genre', back_populates='book_genres', lazy="joined")
    
    
class BookGenre(Base):
    __tablename__ = "book_genre"
    
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey('book.id', ondelete='CASCADE'))
    genre_id = Column(Integer, ForeignKey('genre.id'))#TODO: on_delete
    

class BookAuthor(Base):
    __tablename__ = "book_author"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    book_id = Column(Integer, ForeignKey('book.id', ondelete='CASCADE'))
    role = Column(Integer, ForeignKey('role.id'))
    

class BookPart(Base):
    __tablename__ = "book_part"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    book_id = Column(Integer, ForeignKey('book.id', ondelete='CASCADE'))
    text_id = Column(Integer, ForeignKey('text.id', ondelete='CASCADE'))
    part_order = Column(Integer, nullable=False)