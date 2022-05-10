from fastapi import FastAPI, APIRouter

from .auth.routes import router as user_routes
from .jwt.routes import router as token_routes
from .indexer.routes import router as indexer_routes

router = APIRouter()
router.include_router(user_routes, tags=["users"])
router.include_router(token_routes, tags=["token"])
router.include_router(indexer_routes, tags=["indexer"])

description = """

# Challenge de EpicIO - supercalifragilisticoespiralidoso

Api que da acceso a los datos del microservicio de detección de alertas  
Implementa también una creación de usuarios **muuuuyyy básica**, para permitir  
asegurar los endpoints con jwt.
"""

app = FastAPI(
    title="Indexer Api",
    description=description,
    version="0.0.1",
    contact={
        "name": "Pablo Daniel Rey",
        "url": "http://github.com/pablodanielrey",
        "email": "pablodanielrey@gmail.com"
    }
)
app.include_router(router)
