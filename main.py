from contextlib import asynccontextmanager

from fastapi import FastAPI
from services.authenticate.routes import auth_router
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis


@asynccontextmanager
async def startup_event(app: FastAPI):
    redis = aioredis.from_url(url='redis://5.23.49.44:6379', encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield


app = FastAPI(title='Test App', lifespan=startup_event)
app.include_router(auth_router)
