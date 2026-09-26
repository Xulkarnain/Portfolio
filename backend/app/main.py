from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import ResourceNotFoundException


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)


@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_handler(
    request: Request,
    exc: ResourceNotFoundException,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc),
        },
    )


app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Portfolio API is running"}