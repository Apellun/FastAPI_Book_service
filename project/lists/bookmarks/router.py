from fastapi import Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import lists.bookmarks.service as bookmarks_service
from schemas import (
    BookmarksRead, BookmarkCreate
)
from core.db import get_db
from auth.base_config import user
# from lists.router import lists_router

@lists_router.get('/bookmarks/', tags=["lists"], status_code=200, response_model=List[BookmarksRead])
async def get_all(user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await bookmarks_service.get_bookmarks(user.id, db)
    return result

@lists_router.post('/bookmarks/', tags=["lists"], status_code=201)
async def post(new_bookmark: ListCreate, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await bookmarks_service.add_bookmark(new_bookmark, user.id, db)
    return result

@lists_router.delete('/bookmarks/', tags=["lists"], status_code=204)
async def delete(text_id: int = None, book_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await bookmarks_service.delete_bookmark(text_id, book_id, user.id, db)
    return result
