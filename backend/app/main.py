from fastapi import FastAPI

from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.get("/")
def root():
    return {"message": "Portfolio API is running"}