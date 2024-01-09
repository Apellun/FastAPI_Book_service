from fastapi import Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import lists.finished.service as finished_service
from lists.finished.schemas import FinishedRead, FinishedAdd
from core.db import get_db
from auth.base_config import user
from lists.router import lists_router

@lists_router.get('/finished_reading', tags=["lists"], status_code=200, response_model=List[FinishedRead])
async def get(favorites: bool = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await finished_service.get_finished(user.id, db, favorites)
    return result

@lists_router.post('/finished_reading', tags=["lists"], status_code=201, response_model=List[FinishedRead])
async def post(new_finished: FinishedAdd, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await finished_service.add_finished(new_finished, user.id, db)
    return result

@lists_router.delete('/finished_reading', tags=["lists"], status_code=204)
async def delete(text_id: int = None, book_id: int = None, favorites: bool = None, finished: bool = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await finished_service.delete_finished(favorites, finished,text_id, book_id, user.id, db)
    return result