from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi.exceptions import HTTPException
from datetime import datetime
from texts.models import Text, TextGenre, TextAuthor
from books.models import BookPart
from texts.schemas import TextCreate, TextUpdate
from core.schemas import NewAuthorsData
import texts.utils as utils


async def get_one_by_id(text_id: int, db: AsyncSession):
    text_result = await db.execute(
        select(Text)
        .options(joinedload(Text.creators),
                 joinedload(Text.genres),
                 joinedload(Text.books))
        .where(Text.id == text_id)
    )
    text = text_result.scalars().unique().one()
    return text


async def get_all(genre_id: int, author_id: int, db: AsyncSession):
    if author_id and genre_id:
        query = (select(Text)
        .join(TextGenre)
        .join(TextAuthor)
        .where(
            Text.is_public == True,
            Text.is_singular == True,
            TextGenre.genre_id == genre_id,
            TextAuthor.author_id == author_id)
        )
    elif author_id:
        query = (select(Text)
        .join(TextAuthor)
        .where(
            Text.is_public == True,
            Text.is_singular == True,
            TextAuthor.author_id == author_id)
        )
    elif genre_id:
        query = (select(Text)
        .join(TextGenre)
        .where(
            Text.is_public == True,
            Text.is_singular == True,
            TextGenre.genre_id == genre_id)
        )
    else:
        query = (select(Text)
        .where(Text.is_public == True,
               Text.is_singular == True,)
        .options(joinedload(Text.creators),
                 joinedload(Text.genres),
                 joinedload(Text.books))
        )
    
    texts_result = await db.execute(query)
    texts = texts_result.scalars().unique().all()
    return texts
    

async def get_all_by_author(author_id: int, db: AsyncSession):
    texts_result = await db.execute(
        select(Text)
        .join(TextAuthor)
        .where(
            TextAuthor.author_id == author_id
            )
    )
    texts = texts_result.scalars().unique().all()
    return texts


async def get_one(text_id: int, user_id: int, db: AsyncSession):
    text = await get_one_by_id(text_id, db)
    if not utils.get_read_permission(text, user_id):
            raise HTTPException(status_code=401)
    return text


async def create(new_text: TextCreate, user_id: int, db: AsyncSession):
    text = Text(
        title=new_text.title,
        content=new_text.content,
        date_created=datetime.utcnow(),
        is_public=new_text.is_public,
        is_singular=new_text.is_singular
    )
    
    db.add(text)
    await db.flush()
    
    if new_text.genres:
        print("SEES")
        for genre in new_text.genres:
            print("GENRE", genre)
            text_genre = TextGenre(text_id=text.id, genre_id=genre)
            db.add(text_genre)
        
    text_author = TextAuthor(author_id=user_id, text_id=text.id, role=1)
    db.add(text_author)
    
    await db.commit()
    await db.refresh(text)
    return text


async def update(text_id: int, new_data: TextUpdate, user_id: int, db: AsyncSession): #TODO: check genres + date_updated
    text = await get_one_by_id(text_id, db)
    
    if not user_id in [creator.id for creator in text.creators]:
        raise HTTPException(status_code=401)
    
    new_data_dict = dict(new_data)
    user_role = await utils.get_role(user_id, text.id, db)
    
    if user_role != 1:
        new_data_dict.pop("is_public")
        new_data_dict.pop("is_singular")
    
    if new_data.genres:
        genres = new_data_dict.pop('genres')
    
        for genre_id in [genre.id for genre in text.genres]:
            if genre_id not in genres:
                text_genre = await db.execute(
                    select(TextGenre)
                    .where(TextGenre.text_id == text.id,
                        TextGenre.genre_id == genre_id)
                    )
                text_genre = text_genre.scalars().unique().one()
                await db.delete(text_genre)
            else:
                genres.remove(genre_id)
                
        for genre in genres:
            text_genre = TextGenre(text_id=text.id, genre_id=genre)
            db.add(text_genre)
                
    for key, value in new_data_dict.items():
        if value is not None:
            setattr(text, key, value)
        
    text.date_updated = datetime.utcnow()
    db.add(text)
    
    await db.flush()
    await db.commit()
    await db.refresh(text)
    return text


async def partial_update(text_id: int, new_authors_data: NewAuthorsData, user_id: int, db: AsyncSession):
    text = await get_one_by_id(text_id, db)
    
    if not user_id in [creator.id for creator in text.creators]:
        raise HTTPException(status_code=401)
    else:
        user_role = await utils.get_role(user_id, text.id, db)
        if user_role != 1:
            raise HTTPException(status_code=401)

    try:
        new_authors_data.authors.pop(str(user_id))
    except:
        pass
    
    for author_id, role in new_authors_data.authors.items():
        author_id = int(author_id)
        text_author = await db.execute(
            select(TextAuthor)
            .where(TextAuthor.text_id == text_id,
                   TextAuthor.author_id == author_id
                   )
            )
        try:
            text_author = text_author.scalars().unique().one()
            if role != 1:
                text_author.role = role
                db.add(text_author)
                
        except NoResultFound:
            if role != 1:
                new_text_author = TextAuthor(
                    text_id = text_id,
                    author_id = author_id,
                    role = role)
            
                db.add(new_text_author)
        
    db.add(text)
    await db.flush()
    await db.commit()
    await db.refresh(text)
    
    return text
    

async def delete(text_id: int, user_id: int, db: AsyncSession):
    text = await get_one_by_id(text_id, db)
    
    if not user_id in [creator.id for creator in text.creators]:
        raise HTTPException(status_code=401)
    else:
        user_role = await utils.get_role(user_id, text.id, db)
        if user_role != 1:
            raise HTTPException(status_code=401)
    
    await db.delete(text)
    await db.commit()