from fastapi import FastAPI, status
from src.book.routes import book_router
from src.auth.routes import auth_router
from src.review.routes import review_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from src.db.main import init_db
from .errors import (
    UserAlreadyExist,
    InvalidCredentials,
    InvalidToken,
    BookNotFound,
    UserNotFound,
    TagNotFound,
    TagAlreadyExist,
    InsufficientPermission,
    AccessTokenRequired,
    RefreshTokenRequired,
    RevokedToken,
    create_exception_handler,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("server start")
    await init_db()
    yield
    print("server shutdown")


version = "v1"

app = FastAPI(
    title="bookly",
    description="a REST API for book review web service",
    version=version,
)

app.add_exception_handler(
    UserAlreadyExist,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        inital_detail={
            "message": "user with email exists",
            "error_code": "user exists",
        },
    ),
)

app.add_exception_handler(
    TagAlreadyExist,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        inital_detail={
            "message": "tag already exists",
            "error_code": "tag exists",
        },
    ),
)

app.add_exception_handler(
    UserNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        inital_detail={"message": "user not found", "error_code": "user not found"},
    ),
)

app.add_exception_handler(
    BookNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        inital_detail={"message": "book not found", "error_code": "book not found"},
    ),
)

app.add_exception_handler(
    TagNotFound,
    create_exception_handler(
        status_code=status.HTTP_404_NOT_FOUND,
        inital_detail={"message": "tag not found", "error_code": "tag not found"},
    ),
)

app.add_exception_handler(
    InsufficientPermission,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        inital_detail={
            "message": "you habe no permission",
            "error_code": "insufficent permission",
        },
    ),
)

app.add_exception_handler(
    InvalidToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        inital_detail={
            "message": "invalid token or expired",
            "error_code": "invalid token",
        },
    ),
)

app.add_exception_handler(
    InvalidCredentials,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        inital_detail={
            "message": "invalid email or password",
            "error_code": "invalid credentials",
        },
    ),
)

app.add_exception_handler(
    RevokedToken,
    create_exception_handler(
        status_code=status.HTTP_401_UNAUTHORIZED,
        inital_detail={
            "message": "token invalid or revoked",
            "error_code": "token revoked",
        },
    ),
)

app.add_exception_handler(
    AccessTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        inital_detail={
            "message": "please provide access token",
            "error_code": "access_token_required",
        },
    ),
)

app.add_exception_handler(
    RefreshTokenRequired,
    create_exception_handler(
        status_code=status.HTTP_403_FORBIDDEN,
        inital_detail={
            "message": "please provide valid refresh token",
            "error_code": "refresh_token_required",
        },
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])
