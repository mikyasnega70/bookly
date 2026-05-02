from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import BookService
from .schemas import Book, Bookupdate, BookCreatemodel, BookDetailModel
from src.auth.dependencies import AccessTokenBearer, RoleChecker
from src.errors import BookNotFound
from typing import List

book_router = APIRouter()
book_service = BookService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(['admin', 'user'])

@book_router.get('/', response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_all_books(session:AsyncSession=Depends(get_session), token_details=Depends(access_token_bearer)):
    books = await book_service.get_all_book(session)
    return books

@book_router.get('/user/{user_uid}', response_model=List[Book], dependencies=[Depends(role_checker)])
async def get_user_book_submission(user_uid:str, session:AsyncSession=Depends(get_session), token_details=Depends(access_token_bearer)):
    books = await book_service.get_user_books(user_uid, session)
    return books

@book_router.post('/', status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book_data:BookCreatemodel, session:AsyncSession=Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    user_uid = token_details.get('user')['uid']
    new_book = await book_service.create_book(book_data, user_uid, session)

    return new_book

@book_router.get('/{book_uid}', response_model=BookDetailModel)
async def get_book(book_uid:str, session:AsyncSession=Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    book = await book_service.get_book(book_uid, session)
    if book:
        return book
    else:
        raise BookNotFound()

@book_router.patch('/{book_uid}')
async def update_book(book_uid:str, book_update_data:Bookupdate, session:AsyncSession=Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    updated_book = await book_service.update_book(book_uid, book_update_data, session)

    if updated_book:
        return updated_book
    else:   
        raise BookNotFound()

@book_router.delete('/{book_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_uid:str, session:AsyncSession=Depends(get_session), token_details:dict=Depends(access_token_bearer)):
    book_to_delete = await book_service.delete_book(book_uid, session)

    if book_to_delete:
        return {}
    else: 
        raise BookNotFound()

