from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routers import ClientRouter

config = dotenv_values(".env")

app = FastAPI()


@app.on_event("startup")
def startup_db():
    app.mongodb_client = MongoClient(config["MONGO_URL"])
    app.database = app.mongodb_client[config["MONGO_DB"]]


@app.on_event("shutdown")
def shutdown_db():
    app.mongodb_client.close()


app.include_router(ClientRouter)
