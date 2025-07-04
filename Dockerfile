FROM python:3.11-slim

WORKDIR /app

# Instalar dependências e Docker CLI
RUN apt-get update && \
    apt-get install -y curl gnupg ca-certificates && \
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/debian $(grep VERSION_CODENAME /etc/os-release | cut -d= -f2) stable" > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli && \
    apt-get clean

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY scripts scripts

RUN chmod +x /app/scripts/*

EXPOSE 5000
CMD ["python", "app.py"]
