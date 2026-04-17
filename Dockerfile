FROM python:3.11-slim

WORKDIR /app

COPY server.py .

EXPOSE 5555

CMD ["python", "server.py"]
