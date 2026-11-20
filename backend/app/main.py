from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import DuplicateResourceException, InvalidInputException, InvalidReferenceException, PortfolioOwnerNotFoundException, ResourceNotFoundException

app = FastAPI(title=settings.app_name, debug=settings.debug)

# CORS configuration for local frontend development

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "https://zulkarnain.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
        "Authorization",
        "X-CSRF-Token",
    ],
)



@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "Portfolio API is running"}

@app.exception_handler(DuplicateResourceException)
async def duplicate_resource_handler(request: Request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )

@app.exception_handler(InvalidReferenceException)
async def invalid_reference_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )

@app.exception_handler(InvalidInputException)
async def invalid_input_handler(request: Request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )

@app.exception_handler(PortfolioOwnerNotFoundException)
async def portfolio_owner_not_found_handler(request: Request, exc):
    return JSONResponse(
        status_code=409,
        content={"detail": str(exc)},
    )