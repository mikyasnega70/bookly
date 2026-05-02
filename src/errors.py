from typing import Any, Callable
from fastapi import Request
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
