########################
## indexer journey
##
##########################


para procesar el stream uso un patron como Chain of Responsibility
básicamente tengo una cadena de procesadores y delego el procesamiento del evento a cada uno.


class StreamProcessor(ABC):
    """
    Procesa el stream de eventos de kafka.
    Patrón Chain of Reponsibility
    """

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def process_event(self, detection: Record) -> bool:
        return True


ahi se maneja el orden, y se puede agregar mas procesamientos si es que se requiere.
hoy solo tengo 3.

pablo@xiaomi:/src/github/epic/echallenge/indexer/src/indexer/indexer/stream$ tree
.
├── __init__.py
├── listener.py
├── processor.py
└── processors
    ├── detect_alert.py
    ├── exceptions.py
    ├── __init__.py
    ├── persist_to_db.py
    └── publish_alert.py



---
el procesador de la db


from indexer.vehicles import models

from ..processor import StreamProcessor, Record

class PersistToDB(StreamProcessor):

    def __init__(self, vm: models.VehiclesManager):
        self.vm = vm

    def process_event(self, detection_event: Record) -> bool:
        self.vm.add_detection(timestamp=detection_event.timestamp, **detection_event.value)
        return True


----


el esquema de las detecciones, es una entidad sin nada relacionado.
igualmente pensando en que se podrían agregar procesos al microservicio sobre las detecciones quiero dejar abierta la puerta para poder 
modificar el esquema de la base sin que afecte al código del indexer. o dejarlo lo mas preparado posible.

hoy una detección no tiene tablas relacionadas.
pero tranquilamente se podría tener el concepto de vehículo dentro del sistema, por lo que podrían generar mas entidades, relaciones etc.

pablo@xiaomi:/src/github/epic/echallenge$ docker exec -ti indexer-indexer_pg_db-1 psql -U indexer indexer
psql (14.2 (Debian 14.2-1.pgdg110+1))
Type "help" for help.

indexer=# \dt
           List of relations
 Schema |    Name    | Type  |  Owner  
--------+------------+-------+---------
 public | detections | table | indexer
(1 row)

indexer=# \d detections
                   Table "public.detections"
  Column   |       Type        | Collation | Nullable | Default 
-----------+-------------------+-----------+----------+---------
 id        | uuid              |           | not null | 
 timestamp | bigint            |           |          | 
 year      | integer           |           |          | 
 make      | character varying |           |          | 
 model     | character varying |           |          | 
 category  | character varying |           |          | 
Indexes:
    "detections_pkey" PRIMARY KEY, btree (id)

indexer=# 




class Detection(Base):
    __tablename__ = 'detections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(BigInteger)
    year = Column(Integer)
    make = Column(String)
    model = Column(String)
    category = Column(String)


genero los índices para los métodos que hoy se usan.


class Detection(Base):
    __tablename__ = 'detections'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    timestamp = Column(BigInteger)
    year = Column(Integer)
    make = Column(String, index=True)
    model = Column(String)
    category = Column(String)



----

Recien me doy cuenta que tengo cambiado el orden de los procesadores.

indexer = Indexer(listener, [detect_alert, persist_to_db, publish_to_api])

estaba almacenando solo las alertas!!!.
un simple swap y queda resuelto.


indexer = Indexer(listener, [persist_to_db, detect_alert, publish_to_api])
indexer.start()

----

anda bien el procesamiento del stream.

WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.publish_alert.PublishAlert object at 0x7fbcc3590a90>
WARNING:root:Publicando una alerta timestamp: 1652233576946 vehiculo: {'Year': 2008, 'Make': 'Saturn', 'Model': 'VUE', 'Category': 'SUV'}
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.publish_alert.PublishAlert object at 0x7fbcc3590a90>
WARNING:root:Publicando una alerta timestamp: 1652233577615 vehiculo: {'Year': 2004, 'Make': 'Land Rover', 'Model': 'Discovery', 'Category': 'SUV'}
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.persist_to_db.PersistToDB object at 0x7fbcc3590b20>
WARNING:root:Procesando evento con: <indexer.indexer.stream.processors.detect_alert.DetectAlert object at 0x7fbcc4a3a400>

---

ya tengo un prototipo del indexer desarrollado.
Ahora en cuando a la elección de la base.
para casos genéricos sin mas contexto, uso postgres, porque me da posibilidades de abarcar mas soluciones con una sola tecnología.
inclusive para tablas planas sin realaciones (el peor caso de una base relacional), postgres da buenos resultados con cantidades de registros aceptables, por lo menos para evaluar 
el prototipo inicial.

para este caso!!! 
claramente la base para usar es mongodb o alguna alternativa orientada a documentos no relacional.
pensando en los requerimientos del sistema hoy (sin mas contexto que el de la descripción del challenge)

1 - entidad sin relaciones
2 - formato json
3 - crece infinitamente
4 - no se necesitan consultas complejas. solo una de agregación.
5 - usada por un microservicio el cual podría escalar horizontalmente para abracar x nodos. (debería poder escalar horizontalmente)
6 - el trabajo principal hoy es io bounded. por lo que la implementación debería ser asincrónica!.


para el tema de autenticación de la api es claramente lo contrario.

1 - usuario + auth, 2 entidades relacionadas (a mi entender son separadas. un usuario podría tener mas mecanismos de autenticación)
2 - no es una tabla que crece infinitamente.
3 - tiene un esquema fijo que no debe cambiar, salvo un buen análisis que así lo amerite. (migraciones de esquemas controlada)
4 - posiblemente a futuro se puedan añadir mas entidades relacionadas (métodos de auth adicionales a una clave, ej qr, etc)

para estas entidades el esquema relacional es el mas adecuado. (uso postgres)
solo lo implemento en la api para simplificar y ahorrar tiempo.


-----

ahora tengo implementado en postgres el prototipo, voy a refactorizar para poder manejar 2 tipos de bases de datos para las detecciones.
la lógica detrás de esto es pensando en que el microservicio se puede complejizar a futuro. (por ahi eso acompaña al esquema de datos)
por lo que implemento abstracciones para permitir el cambio hoy de forma simple.

o sea: mongodb y postgresql van a ser una opción de almacenamiento de las detecciones.
NO para la autenticación. la autenticación va a postgres.

-----

despues de refactorizar e implementar las libs para la persistenia en mongo y postgres.
voy a verificar que todo esté funcionando en el indexer.

--

cambio el dockerfile porque agregue una librería adicional. la del protocolo de db.

--

pruebooooo:
pablo@xiaomi:/src/github/epic/echallenge$ docker compose -f docker/docker-compose.indexer-postgres.yml up --remove-orphans

--

lo levante para testearlo dentro del docker. asi que instalo a mano las libs en modo de edicion para poder
modificarlas si veo errores.

pablo@xiaomi:/src/github/epic/echallenge$ docker exec -ti indexer_postgres-indexer-1 bash
root@b5342269a9f1:/usr/app# ls
db  indexer  vehicles_postgres
root@b5342269a9f1:/usr/app# pip install db
^CTraceback (most recent call last):
  File "/usr/local

root@b5342269a9f1:/usr/app# pip install -e db/
Obtaining file:///usr/app/db
  Installing build depend...

root@b5342269a9f1:/usr/app# pip install -e vehicles_postgres/
Obtaining file:///usr/app/vehicles_postgres
  Installi
  
root@b5342269a9f1:/usr/app# pip install -e indexer/
Obtaining file:///usr/app/indexer
  Installing build dependencies ... 


ejecuto el indexer.

root@b5342269a9f1:/usr/app# python3 -m indexer.indexer


y perfecto!!! esta insetando en la base las detecciones.

indexer=# select * from detections limit 10;
                  id                  |   timestamp   | year |     make      |     model      | category 
--------------------------------------+---------------+------+---------------+----------------+----------
 a37a1bd3-08e4-48c8-87bc-5641a391c187 |             1 | 2007 | Ford          | F150 SuperCrew | Pickup
 a2ce140a-ef0f-4358-b565-4c5444a96f07 | 1652214499849 | 2002 | Jeep          | Liberty        | SUV
 9b170213-eb4f-4e7a-9257-f83e415f3253 | 1652214501521 | 1993 | HUMMER        | H1             | SUV
 fcc52572-2d4d-4654-a6df-b6bd0823f603 | 1652214503862 | 2019 | Chevrolet     | Equinox        | SUV
 c29ca2ae-4574-4f57-8faf-db83d407b282 | 1652214504196 | 2011 | Dodge         | Journey        | SUV
 f08b5bbd-338f-43a8-9136-8013300c451f | 1652214506537 | 2019 | Honda         | CR-V           | SUV
 670995f5-0a54-4b2e-8c70-909789c666c2 | 1652214507539 | 1996 | Nissan        | Pathfinder     | SUV
 a9f15548-8433-43db-9bce-6d8b6646f250 | 1652214510548 | 2009 | Jeep          | Liberty        | SUV
 424f0936-a752-403f-ac27-8b2a9ea9ec49 | 1652214511217 | 2010 | Mercedes-Benz | GLK-Class      | SUV
 eef36db0-92b2-4d3f-9619-347f9a552ef4 | 1652214513223 | 2004 | GMC           | Envoy XUV      | SUV
(10 rows)

indexer=# 


--

está insertando a lo loco. todo lo que toma desde kafka.

indexer=# select count(*) from detections;
 count 
-------
  6377
(1 row)

indexer=# select count(*) from detections;
 count 
-------
  6527
(1 row)

indexer=# select count(*) from detections;
 count 
-------
  6594
(1 row)

indexer=# select count(*) from detections;
 count 
-------
  6639
(1 row)

indexer=# select count(*) from detections;
 count 
-------
  6683
(1 row)

indexer=# 

-----

ahora verifico con la lib de mongo a ver si quedó funcionando.
levanto el indexer con la dirección de mongo.


VEHICLES_DB_CONNECTION: mongodb://indexer:superrecontrasecreto@indexer_mongo_db:27017/

root@58cde3c803bb:/usr/app# python3 -m indexer.indexer
WARNING:root:Publicando una alerta timestamp: 1652230308948 vehiculo: {'Year': 2010, 'Make': 'GMC', 'Model': 'Terrain', 'Category': 'SUV'}
WARNING:root:Publicando una alerta timestamp: 1652230309283 vehiculo: {'Year': 2004, 'Make': 'Jeep', 'Model': 'Liberty', 'Category': 'SUV'}
WARNING:root:Publicando una alerta timestamp: 1652230310954 vehiculo: {'Year': 2013, 'Make': 'INFINITI', 'Model': 'FX', 'Category': 'SUV'}
WARNING:root:Publicando una alerta timestamp: 1652230311958 vehiculo: {'Year': 2004, 'Make': 'Acura', 'Model': 'MDX', 'Category': 'SUV'}
WARNING:root:Publicando una alerta t

verifico que esté insertando las alertas en mongo.

pablo@xiaomi:/src/github/epic/echallenge$ docker exec -ti indexer-indexer_mongo_db-1 mongosh -u indexer -p superrecontrasecreto
Current Mongosh Log ID:	627b0f9a68c24faff23ada57
Connecting to:		mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.3.1
Using MongoDB:		5.0.8
Using Mongosh:		1.3.1

For mongosh info see: https://docs.mongodb.com/mongodb-shell/


To help improve our products, anonymous usage data is collected and sent to MongoDB periodically (https://www.mongodb.com/legal/privacy-policy).
You can opt-out by running the disableTelemetry() command.

------
   The server generated these startup warnings when booting:
   2022-05-11T01:17:59.365+00:00: /sys/kernel/mm/transparent_hugepage/enabled is 'always'. We suggest setting it to 'never'
------

test> show databases
admin      102 kB
config    73.7 kB
local     81.9 kB
vehicles   356 kB
test> use vehicles
switched to db vehicles
vehicles> show collections
detections
vehicles> db.detections.find().limit(10)
[
  {
    _id: ObjectId("627af5d0d76b431dcc1f21ef"),
    id: UUID("3800dcf6-6008-4213-80b9-8eb0c5a4cf9b"),
    timestamp: 1,
    year: 2007,
    make: 'Ford',
    model: 'F150 SuperCrew',
    category: 'Pickup'
  },
  {
    _id: ObjectId("627b0f79ff5d702c8002cd54"),
    id: UUID("a956a8c3-a688-49e4-b3f9-c301bc995224"),
    timestamp: Long("1652230308948"),
    year: 2010,
    make: 'GMC',
    model: 'Terrain',
    category: 'SUV'


vehicles> db.detections.count()
DeprecationWarning: Collection.count() is deprecated. Use countDocuments or estimatedDocumentCount.
1310
vehicles> db.detections.count()
1311
vehicles> db.detections.count()
1311
vehicles> db.detections.count()
1311
vehicles> db.detections.count()
1315
vehicles> 


vamooooooooooooooooooooo esta andando la lib también.
perfectoooo

------


documento un poco el código y paso a verificar la api.

---

algunos comentarios sobre la implementación final:

1 - Para las bases relacionales.
use sqlalchemy para no tener que lidiar con la conversión de tipos, y sanitización de datos.
NO elegí implementar la lib de postgres de forma asincrónica debido a que  en la doc de sqlalchemy especifica que esta en fase beta y tengo
mas experiencia con la versión sincrónica. (no quiero estar programando por semanas y debuggeando problemas)

https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html

"""
Tip
The asyncio extension as of SQLAlchemy 1.4.3 can now be considered to be beta level software. API details are subject to change however at this point it is unlikely for there to be significant backwards-incompatible changes.
"""

igualmente tengo claro que para este tipo de soluciones io bounded lo mejor son las versiones async.


2- Para la base de mongo tamibén use la versión sincrónica.
debido a que no quiero implementar 2 veces la lógica de la capa de la base. (una para lo sincrónico y otro para lo async)
si podría ser un enhancement a las libs de las bases generar las versiones async.


3- Como la base iba a ser sincrónica seguí por el mismo camino con el consumer de kafka.
por lo menos para el indexer es la mejor opción ya que simplifica. (no quería mezclar sincrónico y async).
en este caso, manejar versión sincrónica para la base y async para kafka complejiza la solución.


4- Decisión de diseño, las entidades de la base van a tener un uuid como identificador. 
independientemente de si la base internamente asigna ids propios (mondodb - ObjectId)
independiza la identificación de las entidades de la tecnología de backend usada. 
y usar uuids posibilita la identificación global de las entidades dentro de los microservicios. 
(como nota, por experiencia, ante la duda, ponele un uuid, de ultima después se lo sacas)

