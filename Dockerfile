FROM python:3.13-slim

WORKDIR /app

COPY . .

RUN pip install uv --break-system-packages && \
    uv sync

CMD ["uv", "run", "example/webServices.py"]