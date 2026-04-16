from src.config import Config
import redis.asyncio as redis

token_expiry = 3600
token_blocklist = redis.Redis(host=Config.REDIS_HOST, port=Config.REDIS_PORT, decode_responses=True)

async def jti_to_blocklist(jti:str):
    await token_blocklist.set(name=jti, value="", ex=token_expiry)

async def token_in_blocklist(jti:str) -> bool:
    jti = await token_blocklist.get(jti)

    return jti is not None


