FROM python:3.9

WORKDIR /usr/app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# ADD ./requirements.txt ./
# RUN pip install -r requirements.txt

ADD libs/db ./db
RUN pip install ./db

ADD libs/vehicles_mongo ./vehicles_mongo
RUN pip install ./vehicles_mongo

ADD libs/vehicles_postgres ./vehicles_postgres
RUN pip install ./vehicles_postgres

ADD indexer ./indexer
RUN pip install ./indexer

CMD ["python3", "-m", "indexer.indexer"]
