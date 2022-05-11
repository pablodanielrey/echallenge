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


cuando genero las imagenes con el docker compose, me trae una versión antigua de la libreria de db.
y eso provoca que tire errores al ejecutarse.
voy a probar incrementando las versiones a ver que pasa.

--

me volví loco buscando 2 horas por que no generaba correctamnete los packages de python de la api.
solo contenía el root.
me parece que es:

[options]
packages = find_namespace:

[options.packages.find]
where = src

ya que para unificar los proyectos del microservice use 
named namespaces.

efectivamente era eso. ahora tiene que funcionar todo.
--

bueno sigue con problemas. me esta volviendo loco.
ni con esto

pablo@xiaomi:/src/github/epic/produccion/echallenge$ docker compose -f docker/docker-compose.indexer.yml build api_pg --no-cache
Sending build context to Docker daemon  288.2kB
Step 1/14 : FROM python:3.9
 ---> f033692e2c5a
Step 2/14 : WORKDIR /usr/app
 ---> Running in d1bb96925340
Removing intermediate container d1bb96925340
 ---> 44c5a8e6a857
Step 3/14 : ENV PYTHONDONTWRITEBYTECODE 1


voy a tener que generar un registry de docker en otro compose y pushear los packages ahi.
configurar pipy para sacarlos de ese registry por lo menos.

---

puede llegar a ser el cache de las imagenes de docker.
como el indexer usa la misma base de código, me parece que la api esta usando esa.
aunque --no-cache está explicitado.

voy a generar todas de nuevo.


pablo@xiaomi:/src/github/epic/produccion/echallenge$ docker compose -f docker/docker-compose.indexer.yml build  --no-cache
Sending build context to Docker daemon  295.1kB
Step 1/14 : FROM python:3.9
 ---> f033692e2c5a
Step 2/14 : WORKDIR /usr/ap

---


bueno totalmente el colmo. la genere 100000 veces.

pablo@xiaomi:/src/github/epic/echallenge$ docker compose -f docker/docker-compose.indexer.yml images api_pg
Container           Repository          Tag                 Image Id            Size
indexer-api_pg-1    <none>              <none>              05084a64988e        1.05GB
pablo@xiaomi:/src/github/epic/echallenge$ docker run --rm -ti 05084a64988e bash
root@4269cb2f3810:/usr/app# ls api/
.vscode/              dist/                 readme.txt            requirements_dev.txt  setup.py              tests/                
Dockerfile            pyproject.toml        requirements.txt      setup.cfg             src/                  
root@4269cb2f3810:/usr/app# ls api/
.vscode/              dist/                 readme.txt            requirements_dev.txt  setup.py              tests/                
Dockerfile            pyproject.toml        requirements.txt      setup.cfg             src/                  
root@4269cb2f3810:/usr/app# cd api/
root@4269cb2f3810:/usr/app/api# ls
Dockerfile  dist  pyproject.toml  readme.txt  requirements.txt	requirements_dev.txt  setup.cfg  setup.py  src	tests
root@4269cb2f3810:/usr/app/api# cd dist/
root@4269cb2f3810:/usr/app/api/dist# ls
indexer_api-0.0.2-py3-none-any.whl  indexer_api-0.0.2.tar.gz
root@4269cb2f3810:/usr/app/api/dist# tar -xvzf indexer_api-0.0.2.tar.gz 
indexer_api-0.0.2/
indexer_api-0.0.2/PKG-INFO
indexer_api-0.0.2/pyproject.toml
indexer_api-0.0.2/setup.cfg
indexer_api-0.0.2/setup.py
indexer_api-0.0.2/src/
indexer_api-0.0.2/src/indexer/
indexer_api-0.0.2/src/indexer/api/
indexer_api-0.0.2/src/indexer/api/__init__.py
indexer_api-0.0.2/src/indexer/api/__main__.py
indexer_api-0.0.2/src/indexer/api/app.py
indexer_api-0.0.2/src/indexer_api.egg-info/
indexer_api-0.0.2/src/indexer_api.egg-info/PKG-INFO
indexer_api-0.0.2/src/indexer_api.egg-info/SOURCES.txt
indexer_api-0.0.2/src/indexer_api.egg-info/dependency_links.txt
indexer_api-0.0.2/src/indexer_api.egg-info/not-zip-safe
indexer_api-0.0.2/src/indexer_api.egg-info/requires.txt
indexer_api-0.0.2/src/indexer_api.egg-info/top_level.txt
root@4269cb2f3810:/usr/app/api/dist# 


NO tiene las subcarpetas y ya ajuste todo lo que debia ajustar de setup.cfg.
voy a probar genrarla en mi pc e instalar esa versión generada en el conteneodor.

---

pablo@xiaomi:/src/github/epic/produccion/echallenge/api$ python3 -m build
* Creating virtualenv isolated environment...
* Installing packages in isolated environment... (setuptools>=42.0, wheel)
* Getting dependencies for sdist...
running egg_info
creating src/indexer_api.egg-info
writing src/indexer_api.egg-info/PKG-INFO
writing dependency_links to src/indexer_api.egg-info/dependency_links.txt
writing requirements to src/indexer_api.egg-info/requires.txt
writing top-level names to src/indexer_api.

...


lo genero correctamnete. lo dejo ahi en build y corrijo el dockerfile para que lo saque de ahi.

---


pablo@xiaomi:/src/github/epic/produccion/echallenge$ docker build -f api/Dockerfile .
Sending build context to Docker daemon  1.572MB
Step 1/10 : FROM python:3.9
 ---> f033692

 Successfully built 01dad5d2c0d6
pablo@xiaomi:/src/github/epic/produccion/echallenge$ docker rm --rm -ti 01dad5d2c0d6 bash

root@e56cf4e01f25:/usr/app# ls
api  libs
root@e56cf4e01f25:/usr/app# cd libs/
root@e56cf4e01f25:/usr/app/libs# ls
indexer_vehicles-0.0.2-py3-none-any.whl  indexer_vehicles_mongo-0.0.2-py3-none-any.whl	indexer_vehicles_postgres-0.0.2-py3-none-any.whl
indexer_vehicles-0.0.2.tar.gz		 indexer_vehicles_mongo-0.0.2.tar.gz		indexer_vehicles_postgres-0.0.2.tar.gz

...

root@e56cf4e01f25:/usr/app/libs# pip install *.tar.gz
Processing ./indexer_vehicles-0.0.2.tar.gz
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Processing ./indexer_vehicles_mongo-0.0.2.tar.gz
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Processing ./indexer_vehicles_postgres-0.0.2.tar.gz
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
Collecting pydantic
  Downloading pydantic-1.9.0-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (12.2 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 12.2/12.2 MB 14.5 MB/s eta 0:00:00
Collecting pymongo
  Downloading pymongo-4.1.1-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (471 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 471.3/471.3 KB 8.1 MB/s eta 0:00:00
Collecting psycopg2-binary
  Downloading psycopg2_binary-2.9.3-cp39-cp39-manylinux_2_17_x86_64.manylinux2014_x86_64.whl 

  ....

  oot@e56cf4e01f25:/usr/app/libs# cd ..
root@e56cf4e01f25:/usr/app# ls
api  libs
root@e56cf4e01f25:/usr/app# cd api/
root@e56cf4e01f25:/usr/app/api# ls
indexer_api-0.0.2-py3-none-any.whl  indexer_api-0.0.2.tar.gz
root@e56cf4e01f25:/usr/app/api# pip install indexer_api-0.0.2.tar.gz 
Processing ./indexer_api-0.0.2.tar.gz
  Installing build dependencies ... done
  Getting requirements to build wheel ... done


....

root@e56cf4e01f25:/usr/app# python3 -m indexer.api
INFO:     Started server process [88]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)



FUNCIONAAA!!!-
bueno todo a mano funciona. lo que no se soluciona es la cache extraña de docker.
elimine todas las imagenes, los contenedores, etc.

paso por esa opción


 ---> fc39eef1decd
Step 9/10 : ADD api/dist ./api
 ---> 71eedfaf4082
Step 10/10 : CMD ["python3", "-m", "indexer.api"]
 ---> Running in 2e13da3735ac
Removing intermediate container 2e13da3735ac
 ---> 853cd3e9aef3
Successfully built 853cd3e9aef3
Successfully tagged indexer_api_pg:latest


----


estoy intentando reinstalar docker. 
y veo que tenía miles de volumenes lboqueados.

pablo@xiaomi:/src/github/epic/produccion/echallenge$ sudo apt-get remove --purge docker-ce docker-ce-cli docker-ce-rootless-extras docker-compose-plugin docker-scan-plugin docker.io 
Leyendo lista de paquetes... Hecho
Creando árbol de dependencias... Hecho
Leyendo la información de estado... Hecho
Los paquetes indicados a continuación se instalaron de forma automática y ya no son necesarios.
  aufs-dkms aufs-tools cgroupfs-mount libgtkglext1 libintl-perl libintl-xs-perl libmodule-find-perl libmodule-scandeps-perl libpangox-1.0-0 libproc-processtable-perl libsort-naturally-perl libterm-readkey-perl
  needrestart python3-cached-property python3-docker python3-dockerpty python3-jsonschema python3-pyrsistent python3-websocket slirp4netns tini wmdocker
Utilice «sudo apt autoremove» para eliminarlos.
Los siguientes paquetes se ELIMINARÁN:
  docker-ce* docker-ce-cli* docker-ce-rootless-extras* docker-compose-plugin* docker-scan-plugin* docker.io*
0 actualizados, 0 nuevos se instalarán, 6 para eliminar y 106 no actualizados.
Se liberarán 324 MB después de esta operación.
¿Desea continuar? [S/n] s
(Leyendo la base de datos ... 485334 ficheros o directorios instalados actualmente.)
Desinstalando docker-ce (5:20.10.14~3-0~debian-bullseye) ...
invoke-rc.d: policy-rc.d denied execution of stop.
Desinstalando docker-ce-cli (5:20.10.14~3-0~debian-bullseye) ...
Desinstalando docker-ce-rootless-extras (5:20.10.14~3-0~debian-bullseye) ...
Desinstalando docker-compose-plugin (2.3.3~debian-bullseye) ...
Desinstalando docker-scan-plugin (0.17.0~debian-bullseye) ...
Procesando disparadores para man-db (2.9.4-2) ...
(Leyendo la base de datos ... 485116 ficheros o directorios instalados actualmente.)
Purgando ficheros de configuración de docker.io (20.10.5+dfsg1-1+deb11u1) ...

Nuking /var/lib/docker ...

+ umount -f /var/lib/docker/btrfs
+ btrfs subvolume delete /var/lib/docker/btrfs/subvolumes/fe97302cf225e586f1b0a87270f5a62e45a20c62ca42bf0731f4e16b0f47ea0a
Delete subvolume (no-commit): '/var/lib/docker/btrfs/subvolumes/fe97302cf225e586f1b0a87270f5a62e45a20c62ca42bf0731f4e16b0f47ea0a'
+ btrfs subvolume delete /var/lib/docker/btrfs/subvolumes/fcfd23b57a9bebee8ee2f0cfb18d80ef5af38c6c1f6bf85f75de0106440d870d
Delete subvolume (no-commit): '/var/lib/docker/btrfs/subvolumes/fcfd23b57a9bebee8ee2f0cfb18d80ef5af38c6c1f6bf85f75de0106440d870d'
+ btrfs subvolume delete /var/lib/docker/btrfs/subvolumes/fa62d7f37415a919bf30deb4845547bb3fb0af2dc67eea457afb3ee4cf599774
Delete subvolume (no-commit): '/var/lib/docker/btrfs/subvolumes/fa62d7f37415a919bf30deb4845547bb3fb0af2dc67eea457afb3ee4cf599774'
+ btrfs subvolume delete /var/lib/docker/btrfs/subvolumes/f4ef19ff63e663984ecccf491b73b4a90a7f1eb769ec18cec67d7e2a3af3f4aa
Delete subvolume (no-commit): '/var/lib/docker/btrfs/subvolumes/f4ef19ff63e663984ecccf491b73b4a90a7f1eb769ec18cec67d7e2a3af3f4aa'
+ btrfs subvolume delete /var/lib/docker/btrfs/subvolumes/f35baa126157d905d95f2eba96c1937a273f877707c5dc2047fb2f86940c088b
Delete subvolume (no-commit): '/var/lib/docker/btrfs/subvolumes/f35baa126157d905d95f2eba96c1937a273f877707c5dc2047fb2f86940c088b'
+ btrfs subvolume delete /var/lib/docker/b


---

buenooo cambie la version.
y parece que la genero bien.

pablo@xiaomi:/src/github/epic/produccion/echallenge$ docker compose -f docker/docker-compose.indexer.yml build --no-cache
[+] Building 223.0s (23/23) FINISHED                                                                                                                                                                               
 => [indexer_api_pg internal] load build definition from Dockerfile                                                                                                                                           2.0s
 => => transferring dockerfile: 913B                                                                                                                                                                          0.0s
 => [indexer_indexer_pg internal] load build definition from Dockerfile                                                                                                                                       2.4s
 => => transferring dockerfile: 1.09kB                                                                                                                                                                        0.0s
 => [indexer_api_pg internal] load .dockerignore                                                                                                                                                              2.7s
 => => transferring context: 2B                                                                                                                                                                               0.0s
 => [indexer_indexer_pg internal] load .dockerignore                                                                                                                                                          3.0s
 => => transferring context: 2B                                                                                                                                                                               0.0s
 => [indexer_api_pg internal] load metadata for docker.io/library/python:3.9                                                                                                                                  3.0s
 => [indexer_indexer_pg 1/7] FROM docker.io/library/python:3.9@sha256:dd1ca5845e9c14e6402ebaf59ae92e2fb3235147c12d8e112fb3fb2af7928a0f                                                                       50.3s
 => => resolve docker.io/library/python:3.9@sha256:dd1ca5845e9c14e6402ebaf59ae92e2fb3235147c12d8e112fb3fb2af7928a0f                                                                                           0.7s
 => => sha256:dd1ca5845e9c14e6402ebaf59ae92e2fb3235147c12d8e112fb3fb2af7928a0f 2.35kB / 2.35kB                                                                                                                0.0s
 => => sha256:8ccef93ff3c9e1bb9562d394526cdc6834033a0498073d41baa8b309f4fac20e 2.22kB / 2.22kB                                                                                                                0.0s
 => => sha256:f033692e2c5abe1e0ee34bcca759a3e4432b10b0031174b08d48bcc90d14d68b 8.51kB / 8.51kB                                                                                                                0.0s
 => => sha256:967757d5652770cfa81b6cc7577d65e06d336173da116d1fb5b2d349d5d44127 5.16MB / 5.16MB                                                                                                                0.7s
 => => sha256:6aefca2dc61dcbcd268b8a9861e552f9cdb69e57242faec64ac120d2355a9c1a 54.94MB / 54.94MB                                                                                                              7.3s
 => => sha256:c357e2c68cb3bf1e98dcb3eb6ceb16837253db71535921d6993c594588bffe04 10.87MB / 10.87MB                                                                                                              1.8s
 => => sha256:c766e27afb21eddf9ab3e4349700ebe697c32a4c6ada6af4f08282277a291a28 54.58MB / 54.58MB                                                                                                              5.4s
 => => sha256:32a180f5cf85702e7680719c40c39c07972b1176355df5a621de9eb87ad07ce2 196.70MB / 196.70MB                                                                                                           13.9s
 => => sha256:1535e3c1181a81ea66d5bacb16564e4da2ba96304506598be39afe9c82b21c5c 6.29MB / 6.29MB                                                                                                                6.7s
 => => sha256:6de7cb7bdc8f9b4c4d6539233fe87304aa1a6427c3238183265c9f02d831eddb 18.31MB / 18.31MB                                                                                                              9.4s
 => => extracting sha256:6aefca2dc61dcbcd268b8a9861e552f9cdb69e57242faec64ac120d2355a9c1a                                                                                                                     2.6s
 => => sha256:26787c68cf0c92a778db814d327e283fe1da4434a7fea1f0232dae8002e38f33 233B / 233B                                                                                                                    7.9s
 => => sha256:9952b1051adaff513c99f86765361450af108b12b0073d0ba40255c4e419b481 2.87MB / 2.87MB                                                                                                                9.1s
 => => extracting sha256:967757d5652770cfa81b6cc7577d65e06d336173da116d1fb5b2d349d5d44127                                                                                                                     2.0s
 => => extracting sha256:c357e2c68cb3bf1e98dcb3eb6ceb16837253db71535921d6993c594588bffe04                                                                                                                     0.6s
 => => extracting sha256:c766e27afb21eddf9ab3e4349700ebe697c32a4c6ada6af4f08282277a291a28                                                                                                                     3.0s
 => => extracting sha256:32a180f5cf85702e7680719c40c39c07972b1176355df5a621de9eb87ad07ce2                                                                                                                     9.6s
 => => extracting sha256:1535e3c1181a81ea66d5bacb16564e4da2ba96304506598be39afe9c82b21c5c                                                                                                                     5.4s
 => => extracting sha256:6de7cb7bdc8f9b4c4d6539233fe87304aa1a6427c3238183265c9f02d831eddb                                                                                                                     1.0s
 => => extracting sha256:26787c68cf0c92a778db814d327e283fe1da4434a7fea1f0232dae8002e38f33                                                                                                                     0.0s
 => => extracting sha256:9952b1051adaff513c99f86765361450af108b12b0073d0ba40255c4e419b481                                                                                                                     0.5s
 => [indexer_api_pg internal] load build context                                                                                                                                                              1.7s
 => => transferring context: 40.25kB                                                                                                                                                                          0.0s
 => [indexer_indexer_pg internal] load build context                                                                                                                                                          1.9s
 => => transferring context: 98.99kB                                                                                                                                                                          0.0s
 => [indexer_api_pg 2/7] WORKDIR /usr/app                                                                                                                                                                     1.2s
 => [indexer_api_pg 3/7] RUN pip install build                                                                                                                                                                8.0s
 => [indexer_indexer_pg  4/11] ADD libs/db ./db                                                                                                                                                               2.5s
 => [indexer_api_pg 4/7] ADD libs/db/dist ./libs                                                                                                                                                              1.9s
 => [indexer_api_pg 5/7] ADD libs/vehicles_mongo/dist/ ./libs                                                                                                                                                 2.4s 
 => [indexer_indexer_pg  5/11] RUN python -m build ./db && pip install ./db/dist/indexer_vehicles-0.0.2-py3-none-any.whl                                                                                     42.2s 
 => [indexer_api_pg 6/7] ADD libs/vehicles_postgres/dist/ ./libs                                                                                                                                              1.7s 
 => [indexer_api_pg 7/7] ADD api/dist ./api                                                                                                                                                                   1.5s 
 => [indexer_indexer_pg] exporting to image                                                                                                                                                                   9.2s
 => => exporting layers                                                                                                                                                                                       4.4s
 => => writing image sha256:1056b3dc369b262ddfd756453f5f99cc57fe5621001f0d2e72cda78351fa6984                                                                                                                  0.0s
 => => naming to docker.io/library/indexer_api_pg                                                                                                                                                             0.0s
 => => writing image sha256:6459e7718ba9281b5c3cdb0fca02851d62144ab1037e4463755abc90778c07ec                                                                                                                  0.0s
 => => naming to docker.io/library/indexer_indexer_pg                                                                                                                                                         0.0s 
 => [indexer_indexer_pg  6/11] ADD libs/vehicles_mongo ./vehicles_mongo                                                                                                                                       1.8s 
 => [indexer_indexer_pg  7/11] RUN python -m build ./vehicles_mongo && pip install ./vehicles_mongo/dist/indexer_vehicles_mongo-0.0.2-py3-none-any.whl                                                       33.9s
 => [indexer_indexer_pg  8/11] ADD libs/vehicles_postgres ./vehicles_postgres                                                                                                                                 1.4s
 => [indexer_indexer_pg  9/11] RUN python -m build ./vehicles_postgres && pip install ./vehicles_postgres/dist/indexer_vehicles_postgres-0.0.2-py3-none-any.whl                                              34.9s
 => [indexer_indexer_pg 10/11] ADD indexer ./indexer                                                                                                                                                          1.7s
 => [indexer_indexer_pg 11/11] RUN python -m build ./indexer && pip install ./indexer/dist/indexer_indexer-0.0.2-py3-none-any.whl                                                                            32.9s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
pablo@xiaomi:/src/github/epic/produccion/echallenge$ 



--------------------


no se que paso pero despues de rehacer la imagen durante 2 horas seguidas se solucionó.
tuve que reinstalar docker tambien y eliminar todo el contenido de las imagenes.

----

levante el compose del indexer con los servicios sobre postgres y esta andando bien.
ahora pruebo el de mongo.

---


listo probado con mogno y anda perfecto.

ndexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264553217 vehiculo: {'Year': 2013, 'Make': 'Dodge', 'Model': 'Durango', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264555891 vehiculo: {'Year': 2016, 'Make': 'Honda', 'Model': 'CR-V', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264558232 vehiculo: {'Year': 2016, 'Make': 'INFINITI', 'Model': 'QX50', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264560238 vehiculo: {'Year': 2011, 'Make': 'Jeep', 'Model': 'Liberty', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264561241 vehiculo: {'Year': 2004, 'Make': 'Isuzu', 'Model': 'Axiom', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264562244 vehiculo: {'Year': 2016, 'Make': 'Toyota', 'Model': 'Land Cruiser', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264562913 vehiculo: {'Year': 1995, 'Make': 'Chevrolet', 'Model': 'Blazer', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264563581 vehiculo: {'Year': 2019, 'Make': 'BMW', 'Model': 'X4', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264564584 vehiculo: {'Year': 2010, 'Make': 'Jeep', 'Model': 'Liberty', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264564919 vehiculo: {'Year': 2003, 'Make': 'Honda', 'Model': 'CR-V', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264566925 vehiculo: {'Year': 2013, 'Make': 'Jeep', 'Model': 'Grand Cherokee', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264567593 vehiculo: {'Year': 2005, 'Make': 'Toyota', 'Model': 'Highlander', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264568931 vehiculo: {'Year': 1995, 'Make': 'Jeep', 'Model': 'Wrangler', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264569599 vehiculo: {'Year': 2019, 'Make': 'GMC', 'Model': 'Acadia', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264572273 vehiculo: {'Year': 2006, 'Make': 'INFINITI', 'Model': 'QX', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264572608 vehiculo: {'Year': 2004, 'Make': 'Suzuki', 'Model': 'Grand Vitara', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264573611 vehiculo: {'Year': 2004, 'Make': 'BMW', 'Model': 'X3', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264573945 vehiculo: {'Year': 2018, 'Make': 'Hyundai', 'Model': 'Tucson', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264575282 vehiculo: {'Year': 2007, 'Make': 'Toyota', 'Model': 'RAV4', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264575617 vehiculo: {'Year': 2017, 'Make': 'Subaru', 'Model': 'Forester', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264576285 vehiculo: {'Year': 1998, 'Make': 'Toyota', 'Model': 'RAV4', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando una alerta timestamp: 1652264577288 vehiculo: {'Year': 1994, 'Make': 'GMC', 'Model': 'Jimmy', 'Category': 'SUV'}
indexer_mongo-indexer_mongo-1     | WARNING:root:Publicando un

y las detecciones se ven en la api también.

-----

me dedico a documentar y se lo envío a los chicos.

--