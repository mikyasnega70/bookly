from typing import Any, Callable
from fastapi import Request, FastAPI, status
from fastapi.responses import JSONResponse

class BooklyException(Exception):
    pass

class InvalidToken(BooklyException):
    pass

class RevokedToken(BooklyException):
    pass

class AccessTokenRequired(BooklyException):
    pass

class RefreshTokenRequired(BooklyException):
    pass

class UserAlreadyExist(BooklyException):
    pass

class InvalidCredentials(BooklyException):
    pass

class InsufficientPermission(BooklyException):
    pass

class BookNotFound(BooklyException):
    pass

class TagNotFound(BooklyException):
    pass

class TagAlreadyExist(BooklyException):
    pass

class UserNotFound(BooklyException):
    pass

def create_exception_handler(status_code:int, inital_detail:Any) -> Callable[[Request, Exception], JSONResponse]:
    async def exception_handler(request:Request, exc:BooklyException):
        return JSONResponse(content=inital_detail, status_code=status_code)
    
    return exception_handler

def register_all_errors(app: FastAPI):
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
                "message": "you have no permission",
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
