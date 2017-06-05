#!/usr/bin/env bash
set -e


docker build -t test/nc_user .
docker run \
    --env NC_CONFIGURATION=development \
    -p5000:5000 \
    -v$(pwd)/nc_user:/nc_user \
    test/nc_user
