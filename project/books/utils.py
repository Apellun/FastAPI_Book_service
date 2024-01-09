from sqlalchemy import select
from books.models import BookAuthor


def has_reaing_permission(book, user_id):
    if not book.is_public:
        if not user_id in [author.id for author in book.authors]:
            return False
    return True


async def get_role(book_id, user_id, db):
    role_result = await db.execute(
    select(BookAuthor.role)
    .where(BookAuthor.author_id == user_id,
            BookAuthor.book_id == book_id))
    
    role = role_result.scalars().unique().one()
    return role