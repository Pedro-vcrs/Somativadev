# Imagem base
FROM python:3.11-slim

# Pasta de trabalho dentro do container
WORKDIR /app

# Copia dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código
COPY app.py .

# Porta que será exposta
EXPOSE 8080

# Comando para iniciar o app
CMD ["python", "app.py"]

