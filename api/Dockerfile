FROM python:3.9

WORKDIR /usr/app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# ADD ./requirements.txt ./
# RUN pip install -r requirements.txt
RUN pip install build

ADD libs/db/dist ./libs
# RUN python -m build ./db && pip install ./db/dist/indexer_vehicles-0.0.2-py3-none-any.whl

ADD libs/vehicles_mongo/dist/ ./libs
# RUN python -m build ./vehicles_mongo && pip install ./vehicles_mongo/dist/indexer_vehicles_mongo-0.0.2-py3-none-any.whl

ADD libs/vehicles_postgres/dist/ ./libs
# RUN python -m build ./vehicles_postgres && pip install ./vehicles_postgres/dist/indexer_vehicles_postgres-0.0.2-py3-none-any.whl

ADD api/dist ./api
# RUN python -m build ./api && pip install ./api/dist/indexer_api-0.0.2-py3-none-any.whl

RUN pip install ./libs/indexer_vehicles-0.0.2.tar.gz && \
    pip install ./libs/indexer_vehicles_postgres-0.0.2.tar.gz && \
    pip install ./libs/indexer_vehicles_mongo-0.0.2.tar.gz && \
    pip install ./api/*.tar.gz


CMD ["python3", "-m", "indexer.api"]
