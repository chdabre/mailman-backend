# pull official base image
FROM python:3.9.5-slim

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Standard packages
RUN apt-get update && apt-get install -y --no-install-recommends \
		gnupg2 \
		wget \
        lsb-release \
        gettext \
	&& rm -rf /var/lib/apt/lists/*

# Additional packages needed for build on aarch64/arm64 architecture
RUN /bin/sh -c 'set -ex && \
    ARCH=`uname -m` && \
    if [ "$ARCH" = "aarch64" ]; then \
       echo "Installing build deps for $ARCH" && \
	   export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1 &&\
	   export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1 &&\
	   apt-get update && apt-get install -y --no-install-recommends \
	   	build-essential \
		gcc \
		python3-dev \
		libc-dev \
		libffi-dev \
		libssl-dev \
		libjpeg-dev zlib1g-dev \
		libpq-dev; \
    fi'

# install pipenv
RUN pip install micropipenv[toml]

# install dependencies
COPY ./Pipfile /usr/src/app/Pipfile
COPY ./Pipfile.lock /usr/src/app/Pipfile.lock
RUN micropipenv install --deploy


# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]