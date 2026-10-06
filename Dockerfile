
FROM python:3.11.9


WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 5. Comando para iniciar a aplicação Flask
CMD ["python", "app.py"]