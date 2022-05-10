from fastapi import FastAPI, APIRouter

from .auth.routes import router as user_routes
from .jwt.routes import router as token_routes
from .indexer.routes import router as indexer_routes

router = APIRouter()
router.include_router(user_routes, tags=["users"])
router.include_router(token_routes, tags=["token"])
router.include_router(indexer_routes, tags=["indexer"])

app = FastAPI()
app.include_router(router)
