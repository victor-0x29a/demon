from fastapi import FastAPI
from pymongo import MongoClient

from constants import (
    MONGO_DB,
    MONGO_URL
)
from routers import ClientRouter


app = FastAPI()


@app.on_event("startup")
def startup_db():
    app.mongodb_client = MongoClient(MONGO_URL)
    app.database = app.mongodb_client[MONGO_DB]


@app.on_event("shutdown")
def shutdown_db():
    app.mongodb_client.close()


app.include_router(ClientRouter)
