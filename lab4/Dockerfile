FROM python:3.10-slim

WORKDIR /app

COPY pyproject.toml README.md /app/
RUN pip install --no-cache-dir poetry==1.7.1 \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY src /app/src
COPY models /app/models

ENV PYTHONPATH=/app/src

EXPOSE 8000

CMD ["uvicorn", "mlops_lab4.app:app", "--host", "0.0.0.0", "--port", "8000"]
