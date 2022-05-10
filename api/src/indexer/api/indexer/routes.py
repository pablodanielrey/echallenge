
from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from indexer.vehicles.models import VehiclesManager

from ..jwt.deps import get_jwt_token

from . import models, deps, schemas


router = APIRouter()


@router.get("/detections", dependencies=[Depends(get_jwt_token)])
def get_detections(skip: int = 0, limit: int = 100, vm: VehiclesManager = Depends(deps.get_vehicles_manager)):
    detections = vm.detections(skip, limit)
    return schemas.PaginatedApiResponse(skip=skip, limit=limit, data=detections, size=len(detections))


@router.get('/stats', dependencies=[Depends(get_jwt_token)])
def get_vehicles_by_make(vm: VehiclesManager = Depends(deps.get_vehicles_manager)):
    vehicles = vm.vehicles_by_make()
    return schemas.MultipleResultApiResponse(data=vehicles, size=len(vehicles))
    

######
## hack!! para que openapi.json muestre el correcto mime-type.
## quiero que en openapi.json se muestre el descriptor correcto en vez de "application/json"
## EventSourceResponse tiene implementado como variable de instancia, por lo que no es accesible hasta que no 
## se genera una instancia de la misma. (response_class no es de ayuda en este caso sin el hack)
EventSourceResponse.media_type = "text/event-stream; charset=utf-8"

@router.get('/alerts', dependencies=[Depends(get_jwt_token)])
async def get_alerts_stream(request: Request, 
                            am: models.AlertsManager = Depends(deps.get_alerts_manager),
                            response_class=EventSourceResponse):
    return EventSourceResponse(am.kafka_alerts(request))
