import time
from contextlib import asynccontextmanager

import sentry_sdk
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versioning import VersionedFastAPI, version
from redis import asyncio as aioredis
from sqladmin import Admin
from starlette.middleware import Middleware
from starlette.requests import Request
from prometheus_fastapi_instrumentator import Instrumentator

from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UserAdmin
from app.bookings.router import router as bookings_router
from app.config import settings
from app.database import engine
from app.hotels.router import router as hotels_router
from app.images.router import router as images_router
from app.importer.router import router as import_router
from app.logger import logger
from app.pages.router import router as pages_router
from app.users.router import router as users_router

sentry_sdk.init(
    dsn="https://c7716144a6f59b84e3eaa4c9a5534996@o4507107717218304.ingest.de.sentry.io/4507107720101968",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    logger.info(msg="Connected to Redis")
    yield
    logger.info(msg="Application shutdown")


app = FastAPI()
app.include_router(users_router)
app.include_router(bookings_router)
app.include_router(hotels_router)
app.include_router(pages_router)
app.include_router(images_router)
app.include_router(import_router)


@app.get("/sentry-debug")
async def trigger_error():
    division_by_zero = 1 / 0


app = VersionedFastAPI(app,
                       version_format='{major}',
                       prefix_format='/v{major}',
                       description='Greet users with a nice message',
                       lifespan=lifespan
                       )

app.mount("/static", StaticFiles(directory="app/static"), "static")

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)


instrumentator.instrument(app).expose(app)

@app.middleware('http')
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info("Request execution time", extra={
        "process_time": round(process_time, 4)
    })
    return response


admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(UserAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)
