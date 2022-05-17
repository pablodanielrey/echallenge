#!/bin/bash

###
# espera la api montada en /src/api
# espera las libs montadas en /src/libs
###

cd /src
pip install -e /src/libs/db
pip install -e /src/libs/vehicles_mongo
pip install -e /src/libs/vehicles_postgres

pip install -e /src/api
pip install -r /src/api/requirements_dev.txt
