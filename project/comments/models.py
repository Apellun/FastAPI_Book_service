from datetime import datetime
from sqlalchemy import (
    Column, Integer, String,
    DateTime, ForeignKey, Boolean
)
from core.db import Base
    
class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    author = Column(Integer, ForeignKey('user.id'))
    text_id = Column(Integer, ForeignKey('text.id'))
    content = Column(String, nullable=False)
    date_posted = Column(DateTime, default=datetime.utcnow)
    was_updated = Column(Boolean)