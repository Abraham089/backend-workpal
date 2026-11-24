FROM python:3.12-slim

WORKDIR /back_end

ENV PYTHONPATH=/back_end/src

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction

COPY . .

CMD ["fastapi", "run", "src/backend_workpal/main.py", "--host", "0.0.0.0", "--port", "8000"]