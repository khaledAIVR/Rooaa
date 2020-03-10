FROM python:3.7 as base
ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1
WORKDIR /usr/src/app
COPY requirements.txt  /usr/src/app
RUN pip install -r requirements.txt

FROM base as final
WORKDIR /usr/src/app
COPY . /usr/src/app