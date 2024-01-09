from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from fastapi.exceptions import HTTPException
from lists.models import Readlist, Finished, Bookmark
from lists.schemas import FinishedAdd, BookmarkCreate, ReadlistCreate

#Finished reading

async def get_finished(user_id: int, db: AsyncSession, favorites: bool = None):
    if favorites:
        query = (
        select(Finished)
        .where(
            Finished.user_id == user_id,
            Finished.is_favorite == True)
        )
    else:
        query = (
            select(Finished)
            .where(Finished.user_id == user_id,
                Finished.is_finished == True)
        )
        
    query_result = await db.execute(query)
    finished_reading = query_result.scalars().unique().all()
    return finished_reading

async def get_one(db: AsyncSession, book_id = None, text_id = None):
    if book_id:
        query = (select(Finished)
        .where(Finished.book_id == book_id))
    else:
        query = (select(Finished)
        .where(Finished.text_id == text_id))
            
    finished_result = await db.execute(query)
    finished_book = finished_result.scalars().unique().one()
    return finished_book


async def add_finished(new_book: FinishedAdd, user_id: int, db: AsyncSession): #TODO: check texts for publicity, record for existing
    if new_book.text_id == None and new_book.book_id == None:
        raise HTTPException(status_code=400)
    
    if not new_book.book_id:
        try:
            finished_book = await get_one(db, text_id=new_book.text_id)
        except NoResultFound:
            finished_book = Finished(
            user_id = user_id,
            text_id=new_book.text_id
            )
    else:
        try:
            finished_book = await get_one(db, book_id=new_book.book_id)
        except NoResultFound:
            finished_book = Finished(
            user_id = user_id,
            text_id=new_book.text_id
            )
                    
    if new_book.is_favorite:
        finished_book.is_favorite = True
    else:
        finished_book.is_favorite = False
    
    db.add(finished_book)
    await db.commit()
    
    finished = await get_finished(user_id=user_id, db=db, favorites=False)
    return finished
    
async def delete_finished(text_id: int, book_id: int, favorites: bool, finished: bool, user_id: int, db: AsyncSession):
    if text_id == None and book_id == None:
        raise HTTPException(status_code=400)
    if favorites == None and finished == None:
        raise HTTPException(status_code=400)
    
    if not book_id:
        try:
            query = (delete(Finished)
            .where(Finished.text_id == text_id,
                    Finished.user_id == user_id))
        except:
            pass
    else:
        try:
            query = (delete(Finished)
            .where(Finished.book_id == book_id,
                    Finished.user_id == user_id))
        except:
            pass
        
    await db.execute(query)
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