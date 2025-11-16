from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.crud.tasks import create_tables, drop_tables
from app.api.router import api_router as router_tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    await drop_tables()
    print("Base clear")
    await create_tables()
    print("Read base fro work")
    yield
    print("OFF")


app = FastAPI(lifespan=lifespan)

app.include_router(router_tasks)


@app.get("/")
async def home():
    return {"Hello": "Welcome"}
