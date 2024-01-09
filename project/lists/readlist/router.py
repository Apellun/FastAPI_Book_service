from fastapi import Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import lists.service as lists_service
from lists.schemas import (
    ListRead, BookmarksRead, FinishedAdd,
    BookmarkCreate, ReadlistCreate
)
from core.db import get_db
from auth.base_config import user
from fastapi import APIRouter

lists_router = APIRouter()

#Finished reading

@lists_router.get('/finished_reading', tags=["lists"], status_code=200, response_model=List[ListRead])
async def get(favorites: bool = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.get_finished(user.id, db, favorites)
    return result

@lists_router.post('/finished_reading', tags=["lists"], status_code=201, response_model=List[ListRead])
async def post(new_finished: FinishedAdd, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.add_finished(new_finished, user.id, db)
    return result

@lists_router.delete('/finished_reading', tags=["lists"], status_code=204)
async def delete(text_id: int = None, book_id: int = None, favorites: bool = None, finished: bool = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.delete_finished(favorites, finished,text_id, book_id, user.id, db)
    return result

#Readlist

@lists_router.get('/readlist/', tags=["lists"], status_code=200, response_model=List[ListRead])
async def get(user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.get_readlist(user.id, db)
    return result

@lists_router.post('/readlist/', tags=["lists"], status_code=201)
async def post(new_readlist: ReadlistCreate, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.add_readlist(new_readlist, user.id, db)
    return result

@lists_router.delete('/readlist/', tags=["lists"], status_code=204)
async def delete(text_id: int = None, book_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.delete_readlist(text_id, book_id, user.id, db)
    return result

#Bookmarks

@lists_router.get('/bookmarks/', tags=["lists"], status_code=200, response_model=List[BookmarksRead])
async def get_all(user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.get_bookmarks(user.id, db)
    return result

@lists_router.post('/bookmarks/', tags=["lists"], status_code=201)
async def post(new_bookmark: ReadlistCreate, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.add_bookmark(new_bookmark, user.id, db)
    return result

@lists_router.delete('/bookmarks/', tags=["lists"], status_code=204)
async def delete(text_id: int = None, book_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await lists_service.delete_bookmark(text_id, book_id, user.id, db)
    return result
