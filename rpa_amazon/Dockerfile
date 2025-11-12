FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Google Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar todo el proyecto
COPY . /app/

# Instalar dependencias del robot
RUN pip install --no-cache-dir -r robot/requirements.txt

# Instalar dependencias de la API
RUN pip install --no-cache-dir -r api/requirements.txt

# Exponer puerto de la API
EXPOSE 5000

# Comando por defecto - ejecutar la API
CMD ["python", "api/app.py"]