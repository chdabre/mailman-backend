#!/bin/sh

/usr/local/bin/docker-compose --file docker-compose.prod.yaml exec web ./manage.py migrate