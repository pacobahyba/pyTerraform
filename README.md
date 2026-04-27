# pyTerraform

Dashboard de infraestrutura construído com [Reflex](https://reflex.dev/) (Python), containerizado via Docker e implantado no Google Cloud Platform com Terraform.

## Arquitetura

```
Frontend (SPA estático)          Backend (API)
        │                              │
Google Cloud Storage Bucket     Google Cloud Run
        │                              │
        └──────────── GCP ─────────────┘
                       │
         Artifact Registry (imagem Docker)
```

- **Frontend:** build estático exportado pelo Reflex, hospedado em um bucket do Cloud Storage configurado como SPA
- **Backend:** servidor Reflex rodando em um container no Cloud Run (porta 8080)
- **Infraestrutura:** provisionada inteiramente via Terraform

## Pré-requisitos

- Python 3.13+
- [Terraform](https://developer.hashicorp.com/terraform/install)
- [Docker](https://docs.docker.com/get-docker/)
- [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install)
- Autenticação GCP configurada: `gcloud auth application-default login`

## Configuração local

```bash
# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows
# ou
source .venv/bin/activate    # Linux/macOS

# Instalar dependências
pip install -r requirements.txt

# Rodar em modo desenvolvimento
reflex run
```

A aplicação estará disponível em `http://localhost:3000`.

## Infraestrutura (Terraform)

```bash
cd terraform

# Inicializar providers
terraform init

# Visualizar as mudanças planejadas
terraform plan

# Aplicar a infraestrutura
terraform apply
```

### Recursos provisionados

| Recurso | Tipo | Descrição |
|---------|------|-----------|
| `reflex-repo` | Artifact Registry | Repositório Docker para a imagem do backend |
| `py-terraform-service` | Cloud Run | Serviço do backend (API Reflex) |
| `frontend-pyterraform-*` | Cloud Storage Bucket | Hospedagem do frontend estático (SPA) |

## Build e Deploy

### 1. Build da imagem Docker

```bash
docker build -t us-central1-docker.pkg.dev/<PROJECT_ID>/reflex-repo/py-terraform:latest .
docker push us-central1-docker.pkg.dev/<PROJECT_ID>/reflex-repo/py-terraform:latest
```

### 2. Export do frontend estático

```bash
reflex export --frontend-only --no-zip
# Os assets são gerados em deploy_frontend/
```

### 3. Upload do frontend para o GCS

```bash
gcloud storage cp deploy_frontend/** gs://frontend-pyterraform-<PROJECT_ID>/ --recursive
```

## Estrutura do projeto

```
pyTerraform/
├── pyTerraform/
│   ├── __init__.py
│   └── pyTerraform.py      # Componentes e páginas Reflex
├── terraform/
│   ├── main.tf             # Recursos GCP
│   └── variables.tf        # Variáveis Terraform
├── deploy_frontend/        # Build estático do frontend (gerado)
├── Dockerfile
├── requirements.txt
└── rxconfig.py             # Configuração do app Reflex
```

## Tecnologias

- [Reflex](https://reflex.dev/) 0.9.0 — framework Python fullstack
- [Terraform](https://www.terraform.io/) — infraestrutura como código
- [Google Cloud Run](https://cloud.google.com/run) — backend serverless
- [Google Cloud Storage](https://cloud.google.com/storage) — hospedagem do frontend
- [Docker](https://www.docker.com/) — containerização
