from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import UserCreatemodel, UserModel, UserLoginmodel, UserBooksModel
from .service import UserService
from .utils import verify_password, create_access_token, decode_token
from src.db.main import get_session
from src.db.redis import jti_to_blocklist
from .dependencies import (
    RefreshTokenBearer,
    AccessTokenBearer,
    get_current_user,
    RoleChecker,
)
from datetime import timedelta, datetime
from src.errors import UserAlreadyExist, InvalidCredentials, InvalidToken

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(["admin", "user"])


@auth_router.post(
    "/signup", status_code=status.HTTP_201_CREATED, response_model=UserModel
)
async def create_user_account(
    user_data: UserCreatemodel, session: AsyncSession = Depends(get_session)
):
    email = user_data.email
    user_exist = await user_service.user_exist(email, session)

    if user_exist:
        raise UserAlreadyExist()

    new_user = await user_service.create_user(user_data, session)

    return new_user


@auth_router.post("/login")
async def login_access(
    login_data: UserLoginmodel, session: AsyncSession = Depends(get_session)
):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        passwd_valid = verify_password(password, user.password_hash)
        if passwd_valid:
            access_token = create_access_token(
                user_data={"email": user.email, "uid": str(user.uid), "role": user.role}
            )
            refresh_token = create_access_token(
                user_data={
                    "email": user.email,
                    "uid": str(user.uid),
                    "role": user.role,
                },
                expiry=timedelta(days=2),
                refresh=True,
            )

            return JSONResponse(
                content={
                    "message": "login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": {"email": user.email, "uid": str(user.uid)},
                }
            )

    raise InvalidCredentials()


@auth_router.get("/refresh_token")
async def get_new_access_token(token_details: dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details["exp"]

    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(token_details["user"])
        return JSONResponse(content={"access_token": new_access_token})

    raise InvalidToken()


@auth_router.get("/me", response_model=UserBooksModel)
async def get_current_user(
    user=Depends(get_current_user), _: bool = Depends(role_checker)
):
    return user


@auth_router.get("/logout")
async def logout(token_details: dict = Depends(AccessTokenBearer())):
    jti = token_details["jti"]

    await jti_to_blocklist(jti)
    return JSONResponse(content={"message": "logout"}, status_code=status.HTTP_200_OK)
