from fastapi import Depends, APIRouter
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import texts.service as texts_service
from texts.schemas import TextCreate, TextUpdate, TextRead
from core.schemas import NewAuthorsData
from auth.base_config import user
from core.db import get_db


texts_router = APIRouter()

@texts_router.get('/', status_code=200, response_model=List[TextRead])  #TODO limit+offset
async def get(genre_id: int = None, author_id: int = None, db: AsyncSession = Depends(get_db)):
    result = await texts_service.get_all(genre_id, author_id, db)
    return result

@texts_router.get('/my_texts', status_code=200, response_model=List[TextRead])
async def get(user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await texts_service.get_all_by_author(user.id, db)
    return result

@texts_router.get('/{text_id}', status_code=200, response_model=TextRead)
async def get(text_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await texts_service.get_one(text_id, user.id, db)
    return result

@texts_router.post('/', status_code=201, response_model=TextRead)
async def create(new_text: TextCreate = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await texts_service.create(new_text, user.id, db)
    return result

@texts_router.put('/{text_id}', status_code=200, response_model=TextRead)
async def update(text_id: int = None, new_data: TextUpdate = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await texts_service.update(text_id, new_data, user.id, db)
    return result

@texts_router.patch('/{text_id}', status_code=200, response_model=TextRead)
async def patch(text_id: int = None, new_authors_data: NewAuthorsData = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await texts_service.partial_update(text_id, new_authors_data, user.id, db)
    return result

@texts_router.delete('/{text_id}', status_code=204)
async def delete(text_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await texts_service.delete(text_id, user.id, db)
    return result
        