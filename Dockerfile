from python:3.12.10-slim

WORKDIR /app

COPY requerements.txt .

RUN pip install --no-cache-dir -r requerements.txt

copy . .

CMD ["python", "main.py"]