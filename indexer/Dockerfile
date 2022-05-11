####
# Primera etapa
####

FROM python:3.9

WORKDIR /src

RUN apt-get update && apt-get install -y \
  git \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

ENV TZ=America/Argentina/Buenos_Aires
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN pip install -U pip && pip install -U build

# solo hasta que libere el acceso al repo uso mi key
# ENV GIT_SSH_COMMAND='ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -i /src/id_rsa_github'
# ADD ssh-private-key /src/id_rsa_github
RUN git clone git@github.com:pablodanielrey/echallenge.git ./echallenge

# genero los packages de las libs

RUN python -m build ./echallenge/libs/db && \
    python -m build ./echallenge/libs/vehicles_mongo && \
    python -m build ./echallenge/libs/vehicles_postgres

#genero el package del indexer

RUN python -m build ./echallenge/indexer


####
####   Segunda etapa
####
## ahora si el sistema para produccion

FROM python:3.9-slim-buster

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY --from=0 /src/echallenge/libs/db/dist/indexer_vehicles-0.0.2-py3-none-any.whl ./
COPY --from=0 /src/echallenge/libs/vehicles_mongo/dist/indexer_vehicles_mongo-0.0.2-py3-none-any.whl ./
COPY --from=0 /src/echallenge/libs/vehicles_postgres/dist/indexer_vehicles_postgres-0.0.2-py3-none-any.whl ./
COPY --from=0 /src/echallenge/indexer/dist/indexer_indexer-0.0.2-py3-none-any.whl ./

# instalo el sistema.

RUN pip install -U pip
RUN pip install /src/indexer_vehicles-0.0.2-py3-none-any.whl && \
    pip install /src/indexer_vehicles_mongo-0.0.2-py3-none-any.whl && \
    pip install /src/indexer_vehicles_postgres-0.0.2-py3-none-any.whl && \
    pip install /src/indexer_indexer-0.0.2-py3-none-any.whl


CMD ["python3", "-m", "indexer.indexer"]
