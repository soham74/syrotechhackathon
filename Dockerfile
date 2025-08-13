FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PATH="/venv/bin:$PATH"

RUN python -m venv /venv

WORKDIR /app

COPY pyproject.toml /app/
COPY requirements.txt /app/
RUN . /venv/bin/activate && pip install --upgrade pip && \
    (test -f requirements.txt && pip install -r requirements.txt || true) && \
    pip install gunicorn

COPY . /app

ENV DJANGO_SETTINGS_MODULE=core.settings

CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000"]

