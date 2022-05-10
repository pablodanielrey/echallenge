from typing import Protocol, Optional


from .entities import Detection, CountByMake


class VehiclesManager(Protocol):
  """
  Protocolo de acceso a la base de datos del indexer.
  """


  def detections(self, skip: Optional[int] = None, limit: Optional[int] = None) -> list[Detection]:
      """
      Retorna las detecciones almacenadas en la base.  
      Arguments:  
        - skip: indice incial de la lista de detecciones
        - limit: cantidad de detecciones
      Returns:  
        - una lista de las detecciones almacenadas
      """
      ...


  def add_detection(self, **kw) -> str:
      """
      Agrega una detección a la base de detecciones.
      Arguments:  
        - argumentos nombrados con al menos los campos de la Detection.
      Returns: 
        - id de la detección insertada en la base. (es un uuid por diseño)
      """
      ...


  def vehicles_by_make(self) -> list[CountByMake]:
      """
      Cuenta la cantidad de vehículos que fueron detectados de cierta marca.
      Returns:  
        - lista de vehículos agrupadas por marca.
      """
      ...