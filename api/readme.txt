#########################
## api's journey
##
#################


la api está estructurada en 3 partes principales.
auth
indexer
jwt

pablo@xiaomi:/src/github/epic/echallenge/api/src/indexer$ tree 
.
└── api
    ├── app.py
    ├── auth
    │   ├── deps.py
    │   ├── entities.py
    │   ├── exceptions.py
    │   ├── __init__.py
    │   ├── models.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── settings.py
    ├── db.py
    ├── indexer
    │   ├── deps.py
    │   ├── exceptions.py
    │   ├── __init__.py
    │   ├── models.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── settings.py
    ├── __init__.py
    ├── jwt
    │   ├── deps.py
    │   ├── exceptions.py
    │   ├── __init__.py
    │   ├── models.py
    │   ├── routes.py
    │   ├── schemas.py
    │   └── settings.py
    └── __main__.py


cada uno de los módulos tiene:
deps -- contiene codigo para obtener las dependencias.
models -- donde se manjea la lógica del módulo.
routes -- rutas de las apis dentro de fastapi
entities -- entidades que de la base de datos
exceptions -- excepciones del módulo
schemas -- entidades que se usan para comunicarse con distintas partes del sistema y/o usuario
settings -- configuración (tomada del environment para seguir con la lógica de lo que existía en el challenge)


----

el módulo de jwt es muy simple pero existe debido a que 
se todos los chequeos a nivel del token jwt deberían realizarse ahi.
hoy no se verifica nada salvo la firma, expirado, audiencia e issuer.

se podrían configurar chequeos adicionales que se aplicarían a todo el sistema.

---

el módulo de auth contiene dentro la lógica de autenticación.
no lo generé como librería para no hacer mas largo el challenge.
debería ir externo en una lib aparte de la api. (parecido a las detections)
aca se usa postgres.

---

obtener el stream sse de la api.

swagger io no está mostrando los eventos.
queda cargando indefinidamente esperanodo a que el stream finalice para mostrarlo.
el mediatype de la respuesta es correcto así que adjudico el problema al swagger.
no puedo encontrar nada en internet que referencie el tema pero NO es problema de
EventSourceResponse, ni uvicorn haciendo buffer de las respuestas.
también el mediatype de la respuesta está seteado correctamente.
media_type = "text/event-stream; charset=utf-8"

con cualquier otra herramienta se puede ver el stream de eventos hacia el cliente.
ALTERNATIVA para ver el stream de eventos.

usar el endpoint de login 
/login
para obtener el token y consultar con curl el stream
ej:

curl -X GET -H "Authorization: Bearer eyJhbGc4...0N89-eMVMlZvEI" localhost:8000/alerts

event: alert
data: {'Year': 2020, 'Make': 'Mitsubishi', 'Model': 'Outlander', 'Category': 'SUV'}

event: alert
data: {'Year': 1999, 'Make': 'Suzuki', 'Model': 'Vitara', 'Category': 'SUV'}

event: alert
data: {'Year': 2004, 'Make': 'Isuzu', 'Model': 'Ascender', 'Category': 'SUV'}

event: alert
data: {'Year': 2018, 'Make': 'MAZDA', 'Model': 'CX-3', 'Category': 'SUV'}

event: alert
data: {'Year': 2019, 'Make': 'Jeep', 'Model': 'Renegade', 'Category': 'SUV'}

event: alert
data: {'Year': 2018, 'Make': 'Hyundai', 'Model': 'Santa Fe', 'Category': 'SUV'}

....

con esto se logra ver correctamente el stream.

---

en las apis de usuarios, en caso de errores se retorna siempre 400 - bad request 
para no dar datos adicionales y simplificar tipos de ataques contra la misma.
complica la resolución de problemas, pero mejora un poco la seguridad.

salvo en la api de /login
que efectivamente si no existe el usuario entonces retorna unauthorized.

    except auth_exceptions.UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED) from e


---


ejecuto los tests para verificar que todo funcione correctamente

root@e596395a8bc1:/usr/app/api# pytest
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.9.12, pytest-7.1.2, pluggy-1.0.0
rootdir: /usr/app/api, configfile: pyproject.toml, testpaths: tests
plugins: anyio-3.5.0, dotenv-0.5.2, cov-3.0.0
collected 14 items                                                                                                                                                                                                

tests/test_api_users.py ...                                                                                                                                                                                 [ 21%]
tests/test_db_users.py ......                                                                                                                                                                               [ 64%]
tests/test_jwt.py .....                                                                                                                                                                                     [100%]

---------- coverage: platform linux, python 3.9.12-final-0 -----------
Name                                    Stmts   Miss  Cover
-----------------------------------------------------------
src/indexer/api/__init__.py                 0      0   100%
src/indexer/api/__main__.py                 3      3     0%
src/indexer/api/app.py                     11      0   100%
src/indexer/api/auth/__init__.py            0      0   100%
src/indexer/api/auth/db.py                 22      0   100%
src/indexer/api/auth/deps.py                8      0   100%
src/indexer/api/auth/entities.py           20      0   100%
src/indexer/api/auth/exceptions.py          8      0   100%
src/indexer/api/auth/models.py             49      3    94%
src/indexer/api/auth/routes.py             23     12    48%
src/indexer/api/auth/schemas.py            26      0   100%
src/indexer/api/auth/settings.py            3      0   100%
src/indexer/api/indexer/__init__.py         0      0   100%
src/indexer/api/indexer/deps.py            19     13    32%
src/indexer/api/indexer/exceptions.py       2      0   100%
src/indexer/api/indexer/models.py          23     14    39%
src/indexer/api/indexer/routes.py          20      5    75%
src/indexer/api/indexer/schemas.py         10      0   100%
src/indexer/api/indexer/settings.py         5      0   100%
src/indexer/api/jwt/__init__.py             0      0   100%
src/indexer/api/jwt/deps.py                15      2    87%
src/indexer/api/jwt/exceptions.py           4      0   100%
src/indexer/api/jwt/models.py              31      1    97%
src/indexer/api/jwt/routes.py              20     11    45%
src/indexer/api/jwt/schemas.py             10      0   100%
src/indexer/api/jwt/settings.py             7      0   100%
-----------------------------------------------------------
TOTAL                                     339     64    81%


=============================================================================================== 14 passed in 3.66s ================================================================================================
root@e596395a8bc1:/usr/app/api# 


perfecto. anda todo lo que había testeado.

--

genero el dist para la api para le dockerfile.

root@e596395a8bc1:/usr/app# python3 -m build ./api/
* Creating virtualenv isolated environment...
* Installing packages in isolated environment... (setuptools>=42.0, wheel)
* Getting dependencies for sdist...
running egg_

---

