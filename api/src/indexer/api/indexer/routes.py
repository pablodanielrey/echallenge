
from fastapi import APIRouter, Depends, Request
from sse_starlette.sse import EventSourceResponse

from indexer.vehicles.models import VehiclesManager

from indexer.api.auth.infraestructure.fastapi.deps import get_jwt_token

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
     Tener en cuenta que swagger ui no muestra correctamente el stream.  
     Queda cargando el stream esperando que finalize la conexión para mostrarlo.  
     Como alternativa se puede usar el endpoint de **/login**  
     para obtener un token y utilizar una herramineta como curl para acceder al stream.  
    #### Ej:  
     **curl -X GET -H "Authorization: Bearer eyJhbGc4...0N89-eMVMlZvEI" http://localhost:8000/alerts**  

      event: alert
      data: {'Year': 2014, 'Make': 'Land Rover', 'Model': 'Range Rover', 'Category': 'SUV'}  
      event: alert  
      data: {'Year': 2013, 'Make': 'Buick', 'Model': 'Encore', 'Category': 'SUV'}  
      event: alert  
      data: {'Year': 2007, 'Make': 'Chevrolet', 'Model': 'Suburban 1500', 'Category': 'SUV'}  
      event: alert  
      data: {'Year': 2004, 'Make': 'Land Rover', 'Model': 'Freelander', 'Category': 'SUV'}  

    ### Returns:  
      Stream de eventos sse
    """
    return EventSourceResponse(am.kafka_alerts(request))
