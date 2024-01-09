from sqlalchemy import (
    Boolean, Column, Integer, String,
    DateTime, ForeignKey
)
from sqlalchemy.orm import relationship
from core.db import Base
from core.models import Role, Genre


class TextGenre(Base):
    __tablename__ = "text_genre"
    
    id = Column(Integer, primary_key=True, index=True)
    text_id = Column(Integer, ForeignKey('text.id', ondelete='CASCADE'))
    genre_id = Column(Integer, ForeignKey('genre.id'))
    
    
class Text(Base):
    __tablename__ = "text"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    date_created = Column(DateTime)
    date_updated = Column(DateTime)
    is_public = Column(Boolean)
    is_singular = Column(Boolean)
    
    genres = relationship('Genre', secondary='text_genre', back_populates='text_genres', lazy="joined")
    creators = relationship('User', secondary='text_author', back_populates='texts', lazy="joined")
    books = relationship('Book', secondary='book_part', back_populates='parts', lazy="joined")


class TextAuthor(Base):
    __tablename__ = "text_author"

    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'))
    text_id = Column(Integer, ForeignKey('text.id', ondelete='CASCADE'))
    role = Column(Integer, ForeignKey('role.id'))