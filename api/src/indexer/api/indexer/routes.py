
from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from indexer.vehicles.models import VehiclesManager

from ..jwt.deps import get_jwt_token

from . import models, deps, schemas


router = APIRouter()


@router.get("/detections", dependencies=[Depends(get_jwt_token)])
def get_detections(skip: int = 0, limit: int = 100, vm: VehiclesManager = Depends(deps.get_vehicles_manager)):
    """
    # Endpoint que permite obtener las detecciones registradas por el indexer  
    ### Arguments:
      - skip: indice incial de la lista de detecciones
      - limit: cantidad de detecciones a retornar
    ### Returns:  
      Lista de detecciones registradas
    """
    detections = vm.detections(skip, limit)
    return schemas.PaginatedApiResponse(skip=skip, limit=limit, data=detections, size=len(detections))


@router.get('/stats', dependencies=[Depends(get_jwt_token)])
def get_vehicles_by_make(vm: VehiclesManager = Depends(deps.get_vehicles_manager)):
    """
    # Endpoint que permite obtener estadísticas de los vehículos agrupados por marca  
    ### Returns:
      lista de vehículos agrupados por marca.
    """
    vehicles = vm.vehicles_by_make()
    return schemas.MultipleResultApiResponse(data=vehicles, size=len(vehicles))
    

######
## para que openapi.json muestre el correcto mime-type.
## documentado en : https://fastapi.tiangolo.com/advanced/custom-response/
from fastapi.responses import Response
class SseResponse(Response):
    media_type = "text/event-stream; charset=utf-8"


@router.get('/alerts', dependencies=[Depends(get_jwt_token)], response_class=SseResponse)
async def get_alerts_stream(request: Request, 
                            am: models.AlertsManager = Depends(deps.get_alerts_manager)):
    """
    # Endpoint que permite obtener un stream de eventos de alertas detectadas por el indexer.
    ### Returns:  
      Stream de eventos sse
    """
    return EventSourceResponse(am.kafka_alerts(request))
