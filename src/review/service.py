from fastapi.exceptions import HTTPException
from starlette import status
from src.db.models import Review
from src.auth.service import UserService
from src.book.service import BookService
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import ReviewCreateModel

book_service = BookService()
user_service = UserService()

class ReviewService:
    async def add_review_to_book(self, book_uid:int, user_email:str, review_data:ReviewCreateModel, session:AsyncSession):
        try:
            book = await book_service.get_book(book_uid, session)
            user = await user_service.get_user_by_email(user_email, session)

            if not book or not user:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='book or user not found')
            
            review_data_dict = review_data.model_dump()
            new_review = Review(**review_data_dict)

            new_review.user = user
            new_review.book = book
            
            session.add(new_review)
            await session.commit()
            return new_review
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='oops ... something gets wrong')

