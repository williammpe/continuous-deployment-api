# Continuous Deployment API

API simples e segura que permite executar scripts `.sh` via chamadas HTTP, ideal para automações como CI/CD, reinício de containers, builds personalizados, entre outros.

---

## 📂 Estrutura do Projeto

continuous-deployment-api/
├── app.py # API Flask
├── Dockerfile # Imagem com Python + Docker CLI
├── docker-compose.yaml # Define e sobe o serviço da API
├── requirements.txt # Dependências (Flask)
├── scripts/ # Scripts disponíveis para execução
│ ├── api.sh
│ └── test-service.sh
└── Readme.md # Este arquivo


---

## 🚀 Como Funciona

A API possui um único endpoint que recebe um nome de script (sem extensão) e executa o arquivo `.sh` correspondente da pasta `scripts/`.

### 🔒 Segurança

- Requer autenticação via token Bearer (`Authorization: Bearer <seu_token>`).
- Só permite nomes válidos (`letras`, `números`, `-` e `_`).
- Só executa arquivos `.sh` localizados na pasta `scripts/`.

---

## 🧪 Executando localmente

### Pré-requisitos

- Docker
- Docker Compose

### 1. Clonar o repositório

```bash
git clone https://github.com/williammpe/continuous-deployment-api.git
cd continuous-deployment-api
```

### 2. Subir o container

```bash
docker-compose up --build
```

A API ficará disponível em: http://localhost:5000


### Exemplo de Requisição

```bash
curl -X POST http://localhost:5000/executar-script \
  -H "Authorization: Bearer 1234" \
  -H "Content-Type: application/json" \
  -d '{"script": "test-service"}'
```

Isso executa o script scripts/test-service.sh.

### ⚙️ scripts/*.sh

```bash
#!/bin/bash
CONTAINER="test-service"
echo "Reiniciando ${CONTAINER}..."
docker compose -f /app/projects/${CONTAINER}/docker-compose.yaml up --force-recreate --no-deps -d
echo "${CONTAINER} iniciado!"
```

Os projetos são montados via volume a partir de ./TEMP.

### 🔐 Configuração de Token

```bash
SECRET_TOKEN = "1234"
```

Em produção, você pode movê-lo para uma variável de ambiente com os.getenv("SECRET_TOKEN").

### 📌 Observações

- O container já vem com docker-ce-cli instalado.
- Montagem do socket Docker (/var/run/docker.sock) permite controlar containers do host.
- Scripts precisam ter permissão de execução (chmod +x).

👨‍💻 Autor
- William Morais Pereira
[\LinkedIn](https://www.linkedin.com/in/william-morais-pereira/)