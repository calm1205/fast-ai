from fastapi import FastAPI
from .routers import root, gemini, user
from .database import engine, Base
from . import models  # noqa: F401

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(root.router)
app.include_router(gemini.router)
app.include_router(user.router)
