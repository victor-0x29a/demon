from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import MongoClient

from constants import (
    MONGO_DB,
    MONGO_URL
)
from routers import ClientRouter


app = FastAPI()

main_app_lifespan = app.router.lifespan_context


@asynccontextmanager
async def lifespan_wrapper(app):
    app.mongodb_client = MongoClient(MONGO_URL)
    app.database = app.mongodb_client[MONGO_DB]

    async with main_app_lifespan(app) as maybe_state:
        yield maybe_state

    app.mongodb_client.close()

app.router.lifespan_context = lifespan_wrapper


app.include_router(ClientRouter)
