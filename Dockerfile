FROM python:3.7 as base

ENV PIP_DISABLE_PIP_VERSION_CHECK on
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1


FROM base as dependencies
# Download weights
COPY download_weights.sh ./download_weights.sh
RUN chmod +x ./download_weights.sh
RUN ./download_weights.sh

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install pip==23.0.1
RUN pip install poetry==1.4.2

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false 
RUN poetry install 


FROM base as final
# copy installed deps from dependencies image
COPY --from=dependencies /opt/venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /usr/src/app

# Copying downloaded weights from dependencies image
COPY --from=dependencies yolov3.weights ./yolov3.weights
COPY --from=dependencies nyu.h5 ./nyu.h5

COPY . /usr/src/app
