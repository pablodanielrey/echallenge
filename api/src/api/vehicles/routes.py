
from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from api.jwt.deps import get_jwt_token

from . import models, deps, schemas

router = APIRouter()


@router.get("/detections", dependencies=[Depends(get_jwt_token)])
def get_detections(skip: int = 0, limit: int = 100, vm: models.VehiclesManager = Depends(deps.get_vehicles_manager)):
    detections = vm.detections(skip, limit)
    return schemas.PaginatedApiResponse(skip=skip, limit=limit, data=detections, size=len(detections))


@router.get('/stats', dependencies=[Depends(get_jwt_token)])
def get_vehicles_by_make(vm: models.VehiclesManager = Depends(deps.get_vehicles_manager)):
    vehicles = vm.vehicles_by_make()
    return schemas.MultipleResultApiResponse(data=vehicles, size=len(vehicles))
    

@router.get('/alerts', dependencies=[Depends(get_jwt_token)])
async def get_alerts_stream(request: Request, am: models.AlertsManager = Depends(deps.get_alerts_manager)):
    return EventSourceResponse(am.kafka_alerts(request))

