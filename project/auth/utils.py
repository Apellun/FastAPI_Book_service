from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_users.db import SQLAlchemyUserDatabase
from core.db import get_db
from auth.models import User
from auth.manager import UserManager

async def get_user_db(session: AsyncSession = Depends(get_db)):
    yield SQLAlchemyUserDatabase(session, User)
    
async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)