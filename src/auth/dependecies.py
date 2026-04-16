from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils import decode_token
from src.db.redis import token_in_blocklist

class TokenBearer(HTTPBearer):
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request) -> HTTPAuthorizationCredentials|None:
        creds= await super().__call__(request)

        token = creds.credentials

        token_data = decode_token(token)

        if not self.token_valid(token):
            raise HTTPException(status_code=403, detail={'error':'invalid token or expired', 'resolution':'get new token'})

        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(status_code=403, detail={'error':'invalid token or expired', 'resolution':'get new token'})

        if not token_data:
            raise HTTPException(status_code=403, detail="invalid token")
        
        self.verify_token(token_data)
        
        return token_data

    def token_valid(self, token):
        token_data = decode_token(token)

        return  token_data is not None
    
    def verify_token(self, token_data):
        raise NotImplementedError('please override this method')

class AccessTokenBearer(TokenBearer):
    def verify_token(self, token_data:dict):
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=403, detail="please provide access token")
        
class RefreshTokenBearer(TokenBearer):
    def verify_token(self, token_data):
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=403, detail="please provide refresh token")