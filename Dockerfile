# Usar Python 3.10 como base
FROM python:3.10

# Instalar Git
RUN apt-get update && apt-get install -y git

# Clonar el repositorio con el código fuente
RUN git clone https://github.com/andreigrozescu/open-science-ai-rse.git /app

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias
RUN pip install --no-cache-dir -r docs/requirements.txt

# Ejecutar el script principal
CMD ["python", "scripts/main.py"]
