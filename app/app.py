import os

import uvicorn

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from hashids import Hashids


from db import PostgresDB
from models.alp_url import AlpURL, AlpCreateRequest


app = FastAPI()
db = PostgresDB(os.environ['db'], os.environ['user'], os.environ['password'], os.environ['host'], os.environ['port'])
hashids = Hashids(salt=os.environ['salt'], min_length=7)
hostaddr = os.environ['hostaddr']

@app.on_event("startup")
async def startup_event():
    await db.init()


@app.on_event("shutdown")
async def shutdown_event():
    await db.close()


@app.get("/health")
async def root() -> str:
    return "OK"


@app.get("/{id}")
async def get_url(id: str) -> str:
    id = hashids.decode(id)
    alpUrl = await AlpURL.get(db, id[0])
    return RedirectResponse(alpUrl.url)


@app.post("/alp/")
async def create_url(item: AlpCreateRequest) -> str:
    alpUrl = await AlpURL.create(db, item.url)
    return hostaddr + '/' + hashids.encode(alpUrl.id)


if __name__ == '__main__':
    uvicorn.run("app:app", port=7001, host='127.0.0.1')
