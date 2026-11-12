from fastapi import APIRouter

from app.api.routes import health, projects , skills , experiences , education , certifications , blog , contact 
from app.api.routes.admin import auth



api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health.router)
api_router.include_router(projects.router)
api_router.include_router(skills.router)
api_router.include_router(experiences.router)
api_router.include_router(education.router)
api_router.include_router(certifications.router)
api_router.include_router(blog.router)
api_router.include_router(contact.router)
api_router.include_router(auth.router)