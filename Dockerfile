FROM python:3.12-slim

WORKDIR /back_end

ENV PYTHONPATH=/back_end

COPY . .

RUN pip install poetry \
&& poetry config virtualenvs.create false \
&& poetry install --no-root --no-interaction

CMD [ "sh","-c", "echo canto se esta viniendo ayuda ", "poetry", "run", "fastapi", "dev", "src/backend_workpal/main.py", "--host", "0.0.0.0"]
