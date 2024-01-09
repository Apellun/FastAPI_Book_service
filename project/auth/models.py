from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable
from core.db import Base

class User(SQLAlchemyBaseUserTable, Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active: Column(Boolean, nullable=False)
    is_superuser: Column(Boolean, nullable=False)
    is_verified: Column(Boolean, nullable=False)
    
    books = relationship('Book', secondary='book_author', back_populates='authors', lazy="joined")
    texts = relationship('Text', secondary='text_author', back_populates='creators', lazy="joined")