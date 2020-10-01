FROM python:3.7 as base

ENV PIP_DISABLE_PIP_VERSION_CHECK on
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1


FROM base as dependencies

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install -U pip
RUN pip install poetry --use-feature=2020-resolver

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false \
    && poetry export -f requirements.txt --without-hashes --dev \
    | poetry run pip install --use-feature=2020-resolver -r /dev/stdin  \
    && poetry debug

RUN poetry install --no-interaction --no-ansi


FROM base as final

# copy installed deps from dependencies image
COPY --from=dependencies /opt/venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /usr/src/app
COPY . /usr/src/app