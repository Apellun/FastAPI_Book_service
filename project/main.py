import uvicorn
from fastapi import FastAPI
from auth.base_config import auth_backend
from auth.schemas import UserRead, UserCreate
from auth.base_config import fastapi_users
from texts.router import texts_router
from books.router import books_router
from comments.router import comments_router
from lists.router import lists_router
from core.db import engine, Base

app = FastAPI(
    title="SelfPublisher"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Authentication"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Authentication"],
)

@app.on_event("startup")
async def init_models() -> None:
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        
app.include_router(books_router, prefix="/books", tags=["Books"])
app.include_router(texts_router, prefix="/texts", tags=["Texts"])
app.include_router(comments_router, prefix="/comments", tags=["Comments"])
# app.include_router(lists_router, prefix="/lists", tags=["Lists"])

if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, workers=3)