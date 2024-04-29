from contextlib import asynccontextmanager

import uvicorn
from redis import asyncio as aioredis
from fastapi import FastAPI
from fastapi_cache import FastAPICache

from fastapi_cache.backends.redis import RedisBackend
from services.authenticate.routes import auth_router
from services.admin_service.routes import admin_route


@asynccontextmanager
async def startup_event(app: FastAPI):
    redis = await aioredis.from_url(url='redis://5.23.49.44:6379', encoding='utf-8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield


app = FastAPI(title='Test App', lifespan=startup_event)
app.include_router(auth_router)
app.include_router(admin_route)
#
# if __name__ == '__main__':
#     uvicorn.run(app)
