from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from datetime import datetime
from fastapi.exceptions import HTTPException
from comments.models import Comment
from comments.schemas import CommentCreateUpdate
from comments.utils import check_ownership


async def get_one_by_id(comment_id: int, db: AsyncSession):
    print("ID", comment_id)
    comment_result = await db.execute(
        select(Comment)
        # .options(joinedload(Comment.author))
        .where(Comment.id == comment_id)
    )
    comment = comment_result.scalars().unique().one()
    return comment


async def get_all(text_id: int, db: AsyncSession):
    comments_result = await db.execute(
        select(Comment)
        .where(text_id == text_id)
    )
    comments = comments_result.scalars().unique().all()
    return comments

async def create(text_id: int, new_comment: CommentCreateUpdate, user_id: int, db: AsyncSession):
    comment = Comment(
       author=user_id,
       text_id=text_id,
       content=new_comment.content,
       date_posted=datetime.utcnow(),
       was_updated=False,
    )
    db.add(comment)
    
    await db.commit()
    await db.refresh(comment)
    return comment

async def update(user_id: int, comment_id: int, new_data: CommentCreateUpdate, db: AsyncSession):
    comment = await get_one_by_id(comment_id, db)
    if not  check_ownership(comment.author, user_id):
        raise HTTPException(status_code=401)
    
    comment.content = new_data.content
    comment.was_updated = True
    db.add(comment)
    
    await db.commit()
    await db.refresh(comment)
    return comment

async def delete(comment_id: int, user_id: int, db: AsyncSession):
    comment = await get_one_by_id(comment_id, db)
    if not check_ownership(comment.author, user_id):
        raise HTTPException(status_code=401)
    
    await db.delete(comment)
    await db.commit()