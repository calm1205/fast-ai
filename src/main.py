from fastapi import FastAPI
from .routers import root, gemini

app = FastAPI()

app.include_router(root.router)
app.include_router(gemini.router)
