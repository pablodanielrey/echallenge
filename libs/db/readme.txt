

###########################33
##
## refactoring journey
##
###########################


para dejar una estructura correcta, (aunque no sea necesario para que funcione el challenge - ya lo tengo funcionando con las 2 libs)
armo esta lib que contiene las entidades de entradas y salidas de los modelos.
(api <--> lib) e (indexer <--> lib) 

me gustó manejarlo con modelos de pydantic asi que eso es lo que voy a hacer.
teniendo en cuenta que es nativo en fastapi me parece la mejor opción.

---

listo implementada la interfaz. refactorizo el código de las libs para que lo usen.
también realizo los cambios necesarios en la api e indexer.

uso Protocol debido a que no necesito una clase abstracta y a futuro podría agregar mas protocolos al modelo

---



---

temas a mejorar.

- armar una versión asincrónica de la lib para poder usarlo en fastapi de forma asincrónica.



---

Nota: 

NO elegí implementar la lib de postgres de forma asincrónica debido a que  en la doc de sqlalchemy especifica que esta en fase beta.

https://docs.sqlalchemy.org/en/14/orm/extensions/asyncio.html

"""
Tip
The asyncio extension as of SQLAlchemy 1.4.3 can now be considered to be beta level software. API details are subject to change however at this point it is unlikely for there to be significant backwards-incompatible changes.
"""

así que fui por la versión sincrónica de la base.