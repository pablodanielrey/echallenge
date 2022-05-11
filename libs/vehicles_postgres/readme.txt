


#########################
## vehicles postgres journey
##
###########################




manejo los accesos a la base mediante un contextmanager que obtiene las sesiones.

    @contextlib.contextmanager
    def session(self):
        session = Session(self.engine, future=True)
        try:
            yield session
        finally:
            session.close()

en general me funciona bien ese patrón.


-- 

refactorizo la lib para adecuarse al protocolo: 
indexer.vehicles.models.VehiclesModel

---

perfecto, refactorice y corrí los test y funcionan bien. inclusive unos constraints nuevos que puse.

(env) pablo@xiaomi:/src/github/epic/echallenge/libs/vehicles_postgres$ pytest
=============================================================================================== test session starts ===============================================================================================
platform linux -- Python 3.9.2, pytest-7.1.2, pluggy-1.0.0
rootdir: /src/github/epic/echallenge/libs/vehicles_postgres, configfile: pyproject.toml, testpaths: tests
plugins: dotenv-0.5.2, cov-3.0.0
collected 5 items                                                                                                                                                                                                 

tests/test_detections.py .....                                                                                                                                                                              [100%]

----------- coverage: platform linux, python 3.9.2-final-0 -----------
Name                                 Stmts   Miss  Cover
--------------------------------------------------------
src/indexer/pgvehicles/__init__.py       0      0   100%
src/indexer/pgvehicles/db.py            27      2    93%
src/indexer/pgvehicles/entities.py      12      0   100%
src/indexer/pgvehicles/models.py        32      1    97%
--------------------------------------------------------
TOTAL                                   71      3    96%


================================================================================================ 5 passed in 1.12s ================================================================================================
(env) pablo@xiaomi:/src/github/epic/echallenge/libs/vehicles_postgres$ 


---

ahora entonces a verificar el indexer, la api y quedaría ya todo resuelto.

----