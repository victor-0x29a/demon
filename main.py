from fastapi import FastAPI

from routers import ClientRouter

app = FastAPI()


app.include_router(ClientRouter)
