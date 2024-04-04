from fastapi import FastAPI
from contextlib import asynccontextmanager

from database import get_mongo_connection
from routers import ClientRouter, ServerRouter, AuthRouter


app = FastAPI()

main_app_lifespan = app.router.lifespan_context


@asynccontextmanager
async def lifespan_wrapper(app):
    app.database = get_mongo_connection()

    async with main_app_lifespan(app) as maybe_state:
        yield maybe_state

    app.database.client.close()

app.router.lifespan_context = lifespan_wrapper


app.include_router(ClientRouter)
app.include_router(ServerRouter)
app.include_router(AuthRouter)
