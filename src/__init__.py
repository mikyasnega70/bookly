from fastapi import FastAPI
from src.book.routes import book_router
from src.auth.routes import auth_router
from src.review.routes import review_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def lifespan(app:FastAPI):
    print('server start')
    await init_db()
    yield
    print('server shutdown')


version = 'v1'

app = FastAPI(
    title='bookly',
    description='a REST API for book review web service',
    version=version
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(book_router, prefix=f'/api/{version}/books', tags=['books'])
app.include_router(auth_router, prefix=f'/api/{version}/auth', tags=['auth'])
app.include_router(review_router, prefix=f'/api/{version}/reviews', tags=['reviews'])


