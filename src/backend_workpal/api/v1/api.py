from fastapi import APIRouter
from .auth.routers import router as auth_router
from .users.routers import router as user_router
from .skills.routers import router as skill_router
from .roles.routers import router as role_router

api_router = APIRouter(
  prefix="/v1"
)

api_router.include_router(auth_router)
api_router.include_router(user_router)
api_router.include_router(skill_router)
api_router.include_router(role_router)
