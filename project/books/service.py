from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi.exceptions import HTTPException
from datetime import datetime
from books.models import Book, BookGenre, BookAuthor, BookPart
from books.schemas import BookCreate, BookUpdate
from core.schemas import NewAuthorsData
import books.utils as utils
from texts import utils as text_utils


async def get_one_by_id(book_id: int, db: AsyncSession):
    books_result = await db.execute(
        select(Book)
        .options(joinedload(Book.authors),
                 joinedload(Book.genres),
                 joinedload(Book.parts))
        .where(Book.id == book_id)
    )
    book = books_result.scalars().unique().one()
    return book


async def get_all(db: AsyncSession, genre_id: int = None, author_id: int = None):
    if author_id and genre_id:
        query = (select(Book)
        .join(BookGenre)
        .join(BookAuthor)
        .where(
            Book.is_public == True,
            BookGenre.genre_id == genre_id,
            BookAuthor.author_id == author_id)
        )
    elif author_id:
        query = (select(Book)
        .join(BookAuthor)
        .where(
            Book.is_public == True,
            BookAuthor.author_id == author_id)
        )
    elif genre_id:
        query = (select(Book)
        .join(BookGenre)
        .where(
            Book.is_public == True,
            BookGenre.genre_id == genre_id)
        )
    else:
        query = (select(Book)
        .where(Book.is_public == True)
        )
        
    books_result = await db.execute(query)
    books = books_result.scalars().unique().all()
    return books
    

async def get_all_by_author(author_id: int, db: AsyncSession):
    books_result = await db.execute(
        select(Book)
        .join(BookAuthor)
        .where(
            BookAuthor.author_id == author_id
            )
    )
    books = books_result.scalars().unique().all()
    return books


async def get_one(book_id: int, user_id: int, db: AsyncSession):
    book = await get_one_by_id(book_id, db)
    if not utils.has_reaing_permission(book, user_id):
            raise HTTPException(status_code=401)
    return book


async def create(new_book: BookCreate, user_id: int, db: AsyncSession):
    book = Book(
        title=new_book.title,
        is_completed=new_book.is_completed,
        is_public=new_book.is_public,
        date_created=datetime.utcnow()
    )
    
    db.add(book)
    await db.flush()
    
    if new_book.genres:
        for genre in new_book.genres:
            book_genre = BookGenre(book_id=book.id, genre_id=genre)
            db.add(book_genre)
            
    if new_book.parts: #TODO: check ownership
        for order, part in new_book.parts.items():
            book_part = BookPart(book_id=book.id, text_id=part, part_order=order)
            db.add(book_part)
        
    book_author = BookAuthor(author_id=user_id, book_id=book.id, role=1)
    db.add(book_author)
    
    await db.commit()
    await db.refresh(book)
    return book


async def update(book_id: int,  new_data: BookUpdate, user_id: int, db: AsyncSession): #TODO: check genres + date_updated
    book = await get_one_by_id(book_id, db)
    
    if not user_id in [author.id for author in book.authors]:
        raise HTTPException(status_code=401)
    
    new_data_dict = dict(new_data)
    user_role = await utils.get_role(book.id, user_id, db)
    
    if user_role != 1:
        try:
            new_data_dict.pop("is_public")
        except:
            pass
    if user_role == 3:
        try:
            new_data_dict.pop("genres")
        except:
            pass
    
    if new_data.parts:
        parts = new_data_dict.pop('parts')
        parts_keys = list(parts.keys())
        
        for part_id in [part.id for part in book.parts]:
            part_id_str = str(part_id)
            if part_id_str not in parts_keys:
                book_part = await db.execute(
                    select(BookPart)
                    .where(BookPart.book_id == book.id,
                        BookPart.text_id == part_id)
                    )
                book_part = book_part.scalars().unique().one()
                await db.delete(book_part)
            else:
                parts_keys.remove(part_id_str)
                
        for part in parts_keys: #TODO: test
            try:
                role = await text_utils.get_role(user_id, int(part), db)
                if role != 3:
                    book_part = BookPart(book_id=book.id, text_id=int(part), part_order=parts[part])
                    db.add(book_part)
            except:
                pass
            
    if new_data.genres:
        genres = new_data_dict.pop('genres')
    
        for genre_id in [genre.id for genre in book.genres]:
            if genre_id not in genres:
                book_genre = await db.execute(
                    select(BookGenre)
                    .where(BookGenre.book_id == book.id,
                        BookGenre.genre_id == genre_id)
                    )
                book_genre = book_genre.scalars().unique().one()
                await db.delete(book_genre)
            else:
                genres.remove(genre_id)

        for genre in genres:
            book_genre = BookGenre(book_id=book.id, genre_id=genre)
            db.add(book_genre)
                
    for key, value in new_data_dict.items():
        if value is not None:
            setattr(book, key, value)
        
    book.date_updated = datetime.utcnow()
    db.add(book)
    
    await db.flush()
    await db.commit()
    await db.refresh(book)
    return book


async def partial_update(book_id: int, new_authors_data: NewAuthorsData, user_id: int, db: AsyncSession):
    book = await get_one_by_id(book_id, db)
    
    if not user_id in [author.id for author in book.authors]:
        raise HTTPException(status_code=401)
    else:
        user_role = await utils.get_role(book.id, user_id, db)
        if user_role != 1:
            raise HTTPException(status_code=401)

    try:
        new_authors_data.authors.pop(str(user_id))
    except:
        pass
    
    for author_id, role in new_authors_data.authors.items():
        author_id = int(author_id)
        book_author = await db.execute(
            select(BookAuthor)
            .where(BookAuthor.book_id == book_id,
                   BookAuthor.author_id == author_id
                   )
            )
        
        try:
            book_author = book_author.scalars().unique().one()
            if role != 1:
                book_author.role = role
                db.add(book_author)
                
        except NoResultFound:
            new_book_author = BookAuthor(
                book_id = book_id,
                author_id = author_id,
                role = role)
            
            db.add(new_book_author)
        
    db.add(book)
    await db.flush()
    await db.commit()
    await db.refresh(book)
    
    return book
    

async def delete(book_id: int, user_id: int, db: AsyncSession):
    book = await get_one_by_id(book_id, db)
    
    print("ID", user_id)
    
    if not user_id in [author.id for author in book.authors]:
        raise HTTPException(status_code=401)
    else:
        user_role = await utils.get_role(book.id, user_id, db)
        if user_role != 1:
            raise HTTPException(status_code=401)
    
    await db.delete(book)
    await db.commit()