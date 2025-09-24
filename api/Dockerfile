# Imagen base de Python
FROM python:3.13-slim

# Crear directorio de trabajo
WORKDIR /app/api

# Copiar los archivos del proyecto
COPY . /app/api

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Puerto por defecto para la API
EXPOSE 8000

# Comando por defecto (API)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
