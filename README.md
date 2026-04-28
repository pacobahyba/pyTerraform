# pyTerraform

Dashboard de infraestrutura construído com [Reflex](https://reflex.dev/) (Python), containerizado via Docker e implantado no Google Cloud Platform com Terraform.

## Arquitetura

```
Frontend (SPA estático)          Backend (API)
        │                               │
Google Cloud Storage Bucket     Google Cloud Run
        │                               │
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

Importante: a aplicação **não** possui URL fixa de dashboard no código.
O iframe do Grafana pode ser configurado por arquivo local `appsettings.toml` ou pela variável de ambiente `GRAFANA_DASHBOARD_URL`.

Ordem de prioridade:
1. `GRAFANA_DASHBOARD_URL` (variável de ambiente)
2. `appsettings.toml`

### Opção A: arquivo de configuração (recomendado para portabilidade)

Copie o arquivo de exemplo e preencha a URL:

```powershell
Copy-Item appsettings.toml.example appsettings.toml
```

Edite `appsettings.toml`:

```toml
[grafana]
dashboard_url = "http://localhost:3000/d/<dashboard_uid>/node-exporter-full?orgId=1&kiosk"
```

`appsettings.toml` esta no `.gitignore`, entao cada maquina pode ter seu proprio valor.

### Opção B: variável de ambiente

```powershell
# Criar e ativar o ambiente virtual (Windows)
python -m venv .venv
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& ".\.venv\Scripts\Activate.ps1")

# Instalar dependências
pip install -r requirements.txt

# URL final do dashboard usada no iframe do app
$env:GRAFANA_DASHBOARD_URL="http://localhost:3000/d/<dashboard_uid>/node-exporter-full?orgId=1&kiosk"

# Rodar em desenvolvimento (porta diferente do Grafana)
reflex run --frontend-port 3001
```

Opcional (persistir para novos terminais no Windows):

```powershell
setx GRAFANA_DASHBOARD_URL "http://localhost:3000/d/<dashboard_uid>/node-exporter-full?orgId=1&kiosk"
```

A aplicação estará disponível em `http://localhost:3001`.

## Dashboard local (Grafana + Prometheus + Node Exporter)

Este projeto incorpora no frontend um dashboard local com métricas de CPU, memória, rede e disco.

### 1. Containers usados no ambiente

```powershell
docker run -d --name node-exporter -p 9100:9100 prom/node-exporter
docker run -d --name prometheus -p 9090:9090 prom/prometheus
docker run -d `
  --name grafana `
  -p 3000:3000 `
  -e GF_SECURITY_ALLOW_EMBEDDING=true `
  -e GF_AUTH_ANONYMOUS_ENABLED=true `
  -e GF_AUTH_ANONYMOUS_ORG_ROLE=Viewer `
  grafana/grafana
```

### 2. Configuração do datasource (comando usado)

```powershell
cd "C:\Users\Ação da Cidadania\Documents\projetos\pyTerraform" ; python -c "
import urllib.request, json, base64

creds = base64.b64encode(b'admin:admin').decode()
headers = {'Authorization': f'Basic {creds}', 'Content-Type': 'application/json'}

ds_body = json.dumps({
    'name': 'Prometheus',
    'type': 'prometheus',
    'url': 'http://172.17.0.3:9090',
    'access': 'proxy',
    'isDefault': True
}).encode()

req = urllib.request.Request('http://localhost:3000/api/datasources', data=ds_body, headers=headers, method='POST')
try:
    with urllib.request.urlopen(req) as r:
        resp = json.loads(r.read())
        print('Datasource criado:', resp.get('message', resp))
        ds_uid = resp.get('datasource', {}).get('uid', '')
        print('UID:', ds_uid)
except Exception as e:
    print('Erro:', e)
"
```

### 3. URL final do dashboard (definida via variável de ambiente)

```text
http://localhost:3000/d/<dashboard_uid>/node-exporter-full?orgId=1&kiosk
```

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
