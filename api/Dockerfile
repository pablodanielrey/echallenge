FROM python:3.9

WORKDIR /usr/app

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# ADD ./requirements.txt ./
# RUN pip install -r requirements.txt
ADD libs/vehicles ./vehicles
RUN pip install ./vehicles

ADD api ./api
RUN pip install ./api

CMD ["python3", "-m", "indexer.api"]
