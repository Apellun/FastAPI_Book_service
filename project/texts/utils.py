from sqlalchemy import select
from texts.models import TextAuthor


def get_read_permission(text, user_id):
    if not text.is_public:
        if not user_id in (creator.id for creator in text.creators):
            return False
    return True
    

async def get_role(user_id, text_id, db):
    role_result = await db.execute(
    select(TextAuthor.role)
    .where(TextAuthor.author_id == user_id,
            TextAuthor.text_id == text_id))
    
    role = role_result.scalars().unique().one()
    return role