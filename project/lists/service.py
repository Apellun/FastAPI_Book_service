from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from fastapi.exceptions import HTTPException
from lists.models import Readlist, Reading, Bookmark
from lists.schemas import FinishedAdd, BookmarkCreate, ReadlistCreate

#Finished reading

async def get_finished(favorites: bool, user_id: int, db: AsyncSession):
    if favorites:
        query = (
        select(Reading)
        .where(
            Reading.user_id == user_id,
            Reading.is_favorite == True)
        )
    else:
        query = (
            select(Reading)
            .where(Reading.user_id == user_id,
                Reading.is_finished == True)
        )
        
    query_result = await db.execute(query)
    finished_reading = query_result.scalars().unique().all()
    return finished_reading

async def get_one(is_favorite):
    pass

async def add_finished(new_book: FinishedAdd, user_id: int, db: AsyncSession): #TODO: check texts for publicity, record for existing
    if new_book.text_id == None and new_book.book_id == None:
        raise HTTPException(status_code=400)
    
    if not new_book.book_id:
        try:
            if new_book.is_favorite:
                existing_entry = await get_finished(favorites = True, )
        except:
            pass
            
        new_finished = Reading(
            user_id = user_id,
            text_id=new_book.text_id,
            is_favorite=new_book.is_favorite
        )
    else:
        new_finished = Reading(
            user_id = user_id,
            book_id=new_book.book_id,
            is_favorite=new_book.is_favorite
        )
    
    db.add(new_finished)
    await db.commit()
    await db.refresh()
    
    finished = await get_finished(False, user_id, db)
    return finished
    
async def delete_finished(text_id: int, book_id: int, favorites: bool, finished: bool, user_id: int, db: AsyncSession):
    if text_id == None and book_id == None:
        raise HTTPException(status_code=400)
    if favorites == None and finished == None:
        raise HTTPException(status_code=400)
    
    if book_id:
        query = (delete(Reading)
        .where(Reading.book_id == book_id,
                Reading.user_id == user_id)
        )
        # query = (
        #     select(Reading)
        #     .where(Reading.book_id == book_id,
        #            Reading.user_id == user_id)
        # )
    elif text_id:
        query = (delete(Reading)
        .where(Reading.text_id == text_id,
                Reading.user_id == user_id)
        )
        # query = (
        #     select(Reading)
        #     .where(Reading.text_id == text_id,
        #            Reading.user_id == user_id)
        # )
        
    await db.execute(query)
    # reading = query_result.scalars().unique().one()
    
    # await db.delete(reading)
    await db.commit()
        
#Readlist

async def get_readlist(user_id: int, db: AsyncSession):
    query_result = await db.execute(
        select(Readlist)
        .where(Readlist.user_id == user_id)
    )
    readlist = query_result.scalars().unique().all()
    return readlist

async def add_readlist(new_readlist: ReadlistCreate, user_id: int, db: AsyncSession):
    if new_readlist.text_id == None and new_readlist.book_id == None:
        raise HTTPException(status_code=400)
    
    new_readlist_obj = Readlist(
        user_id = user_id,
        text_id=new_readlist.text_id,
        book_id=new_readlist.book_id,
    )
    
    db.add(new_readlist_obj)
    await db.commit()
    await db.refresh(new_readlist_obj)

async def delete_readlist(text_id: int, book_id: int, user_id: int, db: AsyncSession):
    if text_id == None and book_id == None:
        raise HTTPException(status_code=400)
    
    if book_id:
        query = (delete(Readlist)
        .where(Readlist.book_id == book_id,
                Readlist.user_id == user_id)
        )
        # query = (
        #     select(Readlist)
        #     .where(Readlist.book_id == book_id,
        #            Readlist.user_id == user_id)
        # )
    elif text_id:
        query = (delete(Readlist)
        .where(Readlist.text_id == text_id,
                Readlist.user_id == user_id)
        )
        # query = (
        #     select(Readlist)
        #     .where(Readlist.text_id == text_id,
        #            Readlist.user_id == user_id)
        # )
        
    await db.execute(query)
    # readlist = query_result.scalars().unique().one()
    
    # await db.delete(readlist)
    await db.commit()
    
#Bookmarks

async def get_bookmarks(user_id: int, db: AsyncSession):
    query_result = await db.execute(
        select(Bookmark)
        .where(Bookmark.user_id == user_id)
    )
    bookmarks = query_result.scalars().unique().all()
    return bookmarks

async def add_bookmark(new_bookmark: BookmarkCreate, user_id: int, db: AsyncSession):
    if new_bookmark.text_id == None or new_bookmark.book_id == None:
        raise HTTPException(status_code=400)
    
    new_bookmark_obj = Bookmark(
        user_id = user_id,
        text_id=new_bookmark.text_id,
        book_id=new_bookmark.book_id,
    )
    
    db.add(new_bookmark_obj)
    await db.commit()
    await db.refresh(new_bookmark_obj)
    
async def delete_bookmark(text_id: int, book_id: int, user_id: int, db: AsyncSession):
    if text_id == None and book_id == None:
        raise HTTPException(status_code=400)
    
    if text_id and book_id:
        query = (delete(Bookmark)
        .where(Bookmark.text_id == text_id,
               Bookmark.book_id == book_id,
                Bookmark.user_id == user_id)
        )
        # query = (
        #     select(Bookmark)
        #     .where(Bookmark.book_id == book_id,
        #            Bookmark.text_id == text_id,
        #            Bookmark.user_id == user_id)
        # ) 
    elif book_id:
        query = (delete(Bookmark)
        .where(Bookmark.book_id == book_id,
                Bookmark.user_id == user_id)
        )
        # query = (
        #     select(Bookmark)
        #     .where(Bookmark.book_id == book_id,
        #            Bookmark.user_id == user_id)
        # )
    elif text_id:
        query = (delete(Bookmark)
        .where(Bookmark.text_id == text_id,
                Bookmark.user_id == user_id)
        )
        # query = (
        #     select(Bookmark)
        #     .where(Bookmark.text_id == text_id,
        #            Bookmark.user_id == user_id)
        # )
        
    await db.execute(query)
    # bookmark = query_result.scalars().unique().one()
    
    # await db.delete(bookmark)
    await db.commit()