from fastapi import FastAPI, APIRouter

# refactorizado para ser arquitectura hexagonal
from .auth.infraestructure.fastapi.routes import router as user_routes

# falta refactorizar a arquitectura hexagonal
from .indexer.routes import router as indexer_routes


router = APIRouter()
router.include_router(user_routes, tags=["users"])
router.include_router(indexer_routes, tags=["indexer"])

description = """

# Challenge de EpicIO - SuperCalifragilisticoEspiralidoso

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



###
## TODO: 
# HACK!!. hasta modelarlo correctamente genero un endpoint desde infraestructura para inicializar la base de datos
#
###

from fastapi import Depends
from .auth.infraestructure.fastapi.deps import get_repo as get_auth_repo
from .auth.infraestructure.repo.auth_repository import AuthRepository

@app.get('/inicializar')
def inicializar(auth_repo: AuthRepository = Depends(get_auth_repo)):
    auth_repo.init_repository()
    return {"status":"inicializado"}

