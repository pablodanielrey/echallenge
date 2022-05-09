from fastapi import FastAPI, APIRouter, Depends

from .routes.users import router as user_routes
from .routes.login import router as token_routes

router = APIRouter()
router.include_router(user_routes, tags=["users"])
router.include_router(token_routes, tags=["token"])

app = FastAPI()
app.include_router(router)
