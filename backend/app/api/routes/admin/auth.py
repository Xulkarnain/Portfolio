from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi import Depends
from app.api.dependencies import get_current_admin
from app.models.admin_user import AdminUser
from app.api.dependencies import get_auth_service
from app.core.config import settings
from app.schemas.admin import AdminLoginRequest
from app.services.auth import AuthService
from app.core.security import generate_csrf_token
from app.api.dependencies import require_csrf_token
from app.api.dependencies import require_admin_origin
router = APIRouter(prefix="/admin/auth", tags=["Admin Authentication"])


@router.post(
    "/login",
    dependencies=[Depends(require_admin_origin)],
)
def admin_login(
    
    credentials: AdminLoginRequest,
    response: Response,
    auth_service: AuthService = Depends(get_auth_service),
):
    result = auth_service.authenticate_admin(
        email=credentials.email,
        password=credentials.password,
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    token, admin_id = result
    csrf_token = generate_csrf_token(token)
    is_production = settings.environment == "production"

    response.set_cookie(
        key="admin_access_token",
        value=token,
        httponly=True,
        secure=is_production,
        samesite="none" if is_production else "lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )

    response.set_cookie(
        key="admin_csrf_token",
        value=csrf_token,
        httponly=False,
        secure=is_production,
        samesite="none" if is_production else "lax",
        max_age=settings.access_token_expire_minutes * 60,
        path="/",
    )

    return {
        "message": "Login successful",
        "admin_id": admin_id,
    }

@router.get("/me")
def get_admin_profile(
    current_admin: AdminUser = Depends(get_current_admin),
):
    return {
        "id": current_admin.id,
        "email": current_admin.email,
        "is_active": current_admin.is_active,
    }

