from fastapi import FastAPI, APIRouter

from .auth.routes import router as user_routes
from .jwt.routes import router as token_routes
from .vehicles.routes import router as vehicles_routes

router = APIRouter()
router.include_router(user_routes, tags=["users"])
router.include_router(token_routes, tags=["token"])
router.include_router(vehicles_routes, tags=["vehicles"])

app = FastAPI()
app.include_router(router)
