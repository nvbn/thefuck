ARG PYTHON_VERSION
FROM python:${PYTHON_VERSION}
RUN apt-get update -y
RUN apt-get install -yy --no-install-recommends --no-install-suggests fish tcsh zsh
RUN pip install --upgrade pip
COPY . /src
RUN pip install /src
