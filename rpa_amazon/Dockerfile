FROM python:3.11-slim

# Instalar dependencias del sistema (incluyendo curl)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Instalar Chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-chrome.gpg \
    && echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Instalar ChromeDriver manualmente
RUN CHROMEDRIVER_VERSION=$(curl -sS https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE) && \
    wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/$CHROMEDRIVER_VERSION/linux64/chromedriver-linux64.zip && \
    unzip /tmp/chromedriver.zip -d /tmp && \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm -rf /tmp/chromedriver*

WORKDIR /app

# Copiar archivos de requirements
COPY robot/requirements.txt /app/robot/requirements.txt
COPY api/requirements.txt /app/api/requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r robot/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Copiar el resto del código
COPY . /app/

RUN mkdir -p /app/robot/data

# Verificar instalaciones
RUN which chromedriver && chromedriver --version
RUN which google-chrome && google-chrome --version

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]