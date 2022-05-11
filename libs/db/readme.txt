

###########################33
##
## refactoring journey
##
###########################


para dejar una estructura correcta, (aunque no sea necesario para que funcione el challenge - ya lo tengo funcionando con las 2 libs)
armo esta lib que contiene las entidades de entradas y salidas de los modelos.
(api <--> lib) e (indexer <--> lib) 

me gustó manejarlo con modelos de pydantic asi le doy independencia a esta capa de la tecnología a usar en el backend.
así que eso es lo que voy a hacer.
y teniendo en cuenta que fastapi maneja tambien pydantic me parece la mejor opción.

---

listo implementada la interfaz. refactorizo el código de las libs para que lo usen.
también realizo los cambios necesarios en la api e indexer.

uso Protocol debido a que no necesito una clase abstracta y a futuro podría agregar mas protocolos al modelo para manejar mas funcionalidades.


---

temas a mejorar.

- armar una versión asincrónica de la lib para poder usarlo en fastapi mas eficientemente.

---

