from fastapi import Depends, APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import books.service as books_service
from books.schemas import BookRead, BookCreate, BookUpdate
from core.schemas import NewAuthorsData
from auth.base_config import user
from core.db import get_db


books_router = APIRouter()

@books_router.get('/', status_code=200, response_model=List[BookRead])  #TODO limit+offset
async def get(genre_id: int = None, author_id: int = None, db: AsyncSession = Depends(get_db)):
    result = await books_service.get_all(db, genre_id, author_id)
    return result

@books_router.get('/my_books', status_code=200, response_model=List[BookRead]) #TODO: doesn't work
async def get(user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await books_service.get_all_by_author(user.id, db)
    return result

@books_router.get('/{book_id}', status_code=200, response_model=BookRead)
async def get(book_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await books_service.get_one(book_id, user.id, db)
    return result

@books_router.post('/', status_code=201, response_model=BookRead)
async def create(new_book: BookCreate = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await books_service.create(new_book, user.id, db)
    return result

@books_router.put('/{book_id}', status_code=200, response_model=BookRead)
async def update(book_id: int = None, new_data: BookUpdate = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await books_service.update(book_id, new_data, user.id, db)
    return result

@books_router.patch('/{book_id}', status_code=200, response_model=BookRead)
async def patch(book_id: int = None, new_authors_data: NewAuthorsData = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await books_service.partial_update(book_id, new_authors_data, user.id, db)
    return result

@books_router.delete('/{book_id}', status_code=204)
async def delete(book_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await books_service.delete(book_id, user.id, db)
    return result