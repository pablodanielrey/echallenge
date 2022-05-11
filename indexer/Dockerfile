FROM python:3.9

WORKDIR /usr/app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# ADD ./requirements.txt ./
# RUN pip install -r requirements.txt

#Genero las libs y las instalo dentro del entorno.
#por falta de un servidor de distribución de packages o algo parecido 
#lo hago a mano aca en el dockerfile

RUN pip install build

ADD libs/db ./db
RUN python -m build ./db && pip install ./db/dist/indexer_vehicles-0.0.1-py3-none-any.whl

ADD libs/vehicles_mongo ./vehicles_mongo
RUN python -m build ./vehicles_mongo && pip install ./vehicles_mongo/dist/indexer_vehicles_mongo-0.0.1-py3-none-any.whl

ADD libs/vehicles_postgres ./vehicles_postgres
RUN python -m build ./vehicles_postgres && pip install ./vehicles_postgres/dist/indexer_vehicles_postgres-0.0.1-py3-none-any.whl

ADD indexer ./indexer
RUN python -m build ./indexer && pip install ./indexer/dist/indexer_indexer-0.0.1-py3-none-any.whl

CMD ["python3", "-m", "indexer.indexer"]
