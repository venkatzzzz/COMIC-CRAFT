from fastapi import FastAPI

from .routes import router

app = FastAPI(title="ComicCraft")

app.include_router(router)