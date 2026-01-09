FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml README.md /app/

RUN pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY src /app/src
COPY scripts /app/scripts
COPY configs /app/configs

ENV PYTHONPATH=/app/src

CMD ["python", "scripts/run_experiments.py", "--config", "configs/grid.yaml"]
