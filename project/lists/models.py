from sqlalchemy import Boolean, Column, Integer, ForeignKey
from core.db import Base

class Readlist(Base):
    __tablename__ = "readlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    text_id = Column(Integer, ForeignKey('book.id'))
    text_id = Column(Integer, ForeignKey('text.id'))


class Reading(Base):
    __tablename__ = "finished_reading"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    text_id = Column(Integer, ForeignKey('text.id'))
    is_favorite = Column(Boolean)
    is_finished = Column(Boolean)
    
    
class Bookmark(Base):
    __tablename__ = "bookmark"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    text_id = Column(Integer, ForeignKey('text.id'))