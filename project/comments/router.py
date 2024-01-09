from fastapi import Depends
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
import comments.service as comments_service
from comments.schemas import CommentCreateUpdate, CommentRead
from core.db import get_db
from auth.base_config import user
from fastapi import APIRouter

comments_router = APIRouter()

@comments_router.get('/{text_id}', tags=["comments"], status_code=200, response_model=List[CommentRead]) #TODO: just display with texts
async def get_all(text_id: int = None, db: AsyncSession = Depends(get_db)):
    result = await comments_service.get_all(text_id, db)
    return result

@comments_router.post('/{text_id}', tags=["comments"], status_code=201, response_model=CommentRead)
async def create(text_id: int = None, new_comment: CommentCreateUpdate = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await comments_service.create(text_id, new_comment, user.id, db)
    return result

@comments_router.put('/{comment_id}', tags=["comments"], status_code=200, response_model=CommentRead)
async def put(comment_id: int = None, new_data: CommentCreateUpdate = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await comments_service.update(user.id, comment_id, new_data, db)
    return result

@comments_router.delete('/{comment_id}', tags=["comments"], status_code=204)
async def delete(comment_id: int = None, user = Depends(user), db: AsyncSession = Depends(get_db)):
    result = await comments_service.delete(comment_id, user.id, db)
    return result