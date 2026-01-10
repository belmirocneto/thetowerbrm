# 🏰 Battle Reports Manager

Sistema completo de gerenciamento de relatórios de batalha para o jogo **The Tower Idle Defense**, com frontend React, backend em Python e banco de dados PostgreSQL.

![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat&logo=microsoft-azure&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=flat&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=flat&logo=postgresql&logoColor=white)
![OpenTofu](https://img.shields.io/badge/-OpenTofu-%23c9d1d9?logo=opentofu&logoColor=white)

## 📋 Índice

- [Características](#-características)
- [Arquitetura](#-arquitetura)
- [Pré-requisitos](#-pré-requisitos)
- [Instalação Local](#-instalação-local)
- [Configuração](#-configuração)
- [Deploy na Azure](#-deploy-na-azure)
- [API Documentation](#-api-documentation)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Contribuindo](#-contribuindo)
- [Licença](#-licença)

## ✨ Características

### Frontend (React rodando em um Static WebApp)
- 🌐 **Internacionalização**: Suporte para PT-BR e EN
- 📊 **Visualização de Dados**: Gráficos interativos sincronizados
- 📱 **Responsivo**: Design adaptável para mobile e desktop
- 🎨 **Preparado para até 25 Tiers**: Sistema de cores para identificação visual
- 🔒 **Autenticação**: Sistema utiliza o Account ID (16 caracteres) para persistir os dados
- 📈 **Métricas**: Cálculo automático de runs/day e recursos/day

### Backend (Python rodando em Azure Functions)
- ⚡ **Serverless**: Azure Functions com Python 3.11
- 🔐 **Segurança**: API Key authentication
- 📝 **Parser Inteligente**: Suporte automático para EN e PT-BR
- 🗄️ **PostgreSQL**: Banco de dados escalável
- 📖 **OpenAPI**: Documentação Swagger (local only)

### DevOps
- 🚀 **CI/CD**: GitHub Actions workflows
- 🏗️ **IaC**: OpenTofu para provisionamento
- 🆓 **Free Tier**: Configurado para Azure Free Tier
- 📊 **Monitoramento**: Application Insights

## 🏗️ Arquitetura
```
┌─────────────────────────────────────────────────────────┐
│                    Internet                              │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│     Azure Static Web Apps (Frontend - React)           │
│     - SSL automático                                    │
│     - CDN global                                        │
│     - Deploy via GitHub Actions                         │
└────────────────┬───────────────────────────────────────┘
                 │
                 │ HTTPS + API Key
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│     Azure Functions (Backend - Python)                 │
│     - GetReports (GET /api/reports)                    │
│     - CreateReport (POST /api/reports)                 │
│     - DeleteReport (DELETE /api/reports/{id})          │
│     - Docs (GET /api/docs) - Local only                │
└────────────────┬───────────────────────────────────────┘
                 │
                 │ SSL Connection
                 │
                 ▼
┌────────────────────────────────────────────────────────┐
│     Azure Database for PostgreSQL                      │
│     - Flexible Server B1ms                             │
│     - 20GB Storage                                      │
│     - SSL obrigatório                                   │
└────────────────────────────────────────────────────────┘
```

## 🔧 Pré-requisitos

### Desenvolvimento Local
- **Node.js**: 18.x ou superior
- **Python**: 3.11
- **PostgreSQL**: 14 ou superior
- **Azure Functions Core Tools**: 4.x
- **Azure CLI**: 2.x
- **OpenTofu**: 1.6.x

### Azure (Produção)
- Conta Azure ativa
- Subscription com permissões de Contributor
- GitHub account

## 💻 Instalação Local

### 1. Clonar o Repositório
```bash
git clone https://github.com/yourusername/battle-reports.git
cd battle-reports
```

### 2. Configurar Backend (API)
```bash
cd api

# Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp local.settings.json.example local.settings.json
# Editar local.settings.json com suas credenciais
```

**api/local.settings.json:**
```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "DATABASE_URL": "postgresql://user:password@localhost:5432/battle_reports",
    "API_KEY": "your-dev-api-key-here",
    "FRONTEND_URL": "http://localhost:3000"
  }
}
```

**Criar banco de dados:**
```bash
# PostgreSQL
createdb battle_reports

# Ou via psql
psql -U postgres
CREATE DATABASE battle_reports;
\q
```

**Iniciar API:**
```bash
func start
# API disponível em http://localhost:7071
```

### 3. Configurar Frontend
```bash
cd frontend

# Instalar dependências
npm install

# Criar arquivo de configuração
cp .env.example .env.local
```

**.env.local:**
```env
REACT_APP_API_URL=http://localhost:7071/api
REACT_APP_API_KEY=your-dev-api-key-here
```

**Iniciar Frontend:**
```bash
npm start
# Frontend disponível em http://localhost:3000
```

### 4. Acessar Documentação da API (Local)
```
http://localhost:7071/api/docs
```

## 🔐 Configuração

### Gerar API Key Segura
```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -base64 32
```

### Obter User ID do Jogo

1. Abra o jogo **The Tower**
2. Vá em **Settings** → **Account**
3. Copie o **User ID** (16 caracteres alfanuméricos)

## ☁️ Deploy na Azure

### 1. Preparar OpenTofu
```bash
cd iac

# Copiar arquivo de exemplo
cp terraform.tfvars.example terraform.tfvars

# Editar com seus valores
nano terraform.tfvars
```

**terraform.tfvars:**
```hcl
project_name = "battle-reports"
environment  = "prod"
location     = "East US"

db_admin_username = "adminuser"
db_admin_password = "YourSecurePassword123!"
api_key           = "your-secure-api-key-here"
```

### 2. Provisionar Infraestrutura
```bash
# Login no Azure
az login

# Inicializar OpenTofu
tofu init

# Ver plano de execução
tofu plan

# Aplicar (criar recursos)
tofu apply

# Salvar outputs importantes
tofu output frontend_url > ../FRONTEND_URL.txt
tofu output backend_url > ../BACKEND_URL.txt
tofu output static_web_app_token > ../SWA_TOKEN.txt
```

### 3. Configurar GitHub Secrets

Vá em **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

**Secrets necessários:**
```yaml
# Azure Authentication
AZURE_CREDENTIALS: (JSON do service principal)

# Backend
AZURE_FUNCTION_APP_NAME: func-battle-reports-prod
AZURE_FUNCTION_APP_PUBLISH_PROFILE: (XML do publish profile)

# Frontend
AZURE_STATIC_WEB_APPS_API_TOKEN: (token do Static Web App)
REACT_APP_API_URL: https://func-battle-reports-prod.azurewebsites.net/api
REACT_APP_API_KEY: your-api-key-here

# OpenTofu
DB_ADMIN_USERNAME: adminuser
DB_ADMIN_PASSWORD: YourSecurePassword123!
API_KEY: your-api-key-here
```

**Como obter os secrets:**
```bash
# Service Principal
az ad sp create-for-rbac \
  --name "github-actions-battle-reports" \
  --role contributor \
  --scopes /subscriptions/{subscription-id} \
  --sdk-auth

# Function App Publish Profile
az functionapp deployment list-publishing-profiles \
  --name func-battle-reports-prod \
  --resource-group rg-battle-reports-prod \
  --xml

# Static Web App Token
tofu output static_web_app_token
```

### 4. Deploy Automático

Após configurar os secrets, qualquer push para `main` dispara o deploy:
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

## 📖 API Documentation

### Autenticação

Todas as requisições (exceto `/docs`) requerem o header:
```
X-API-Key: your-api-key-here
```

### Endpoints

#### GET /api/reports
Busca reports de um usuário

**Query Parameters:**
- `user_id` (required): User ID de 16 caracteres
- `limit` (optional): Número de reports por página (default: 15)
- `page` (optional): Número da página (default: 1)

**Exemplo:**
```bash
curl -X GET "http://localhost:7071/api/reports?user_id=7E9CB1C14B2D2025&limit=10&page=1" \
  -H "X-API-Key: your-api-key"
```

#### POST /api/reports
Cria um novo report

**Body:**
```json
{
  "user_id": "7E9CB1C14B2D2025",
  "raw_data": "Battle Report\nBattle Date jan 08, 2026 17:56\n..."
}
```

**Exemplo:**
```bash
curl -X POST "http://localhost:7071/api/reports" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d @report.json
```

#### DELETE /api/reports/{report_id}
Deleta um report

**Exemplo:**
```bash
curl -X DELETE "http://localhost:7071/api/reports/abc-123?user_id=7E9CB1C14B2D2025" \
  -H "X-API-Key: your-api-key"
```

### Swagger UI (Local Only)

Acesse `http://localhost:7071/api/docs` para documentação interativa.

## 📁 Estrutura do Projeto
```
battle-reports/
├── .github/
│   └── workflows/          # GitHub Actions CI/CD
│       ├── backend-deploy.yml
│       ├── frontend-deploy.yml
│       ├── tofu-plan.yml
│       └── tofu-apply.yml
│
├── frontend/              # React Application
│   ├── public/
│   ├── src/
│   │   ├── BattleReportApp.js  # Componente principal
│   │   ├── config.js           # Configuração da API
│   │   └── index.js
│   ├── package.json
│   └── .env.example
│
├── api/                   # Azure Functions (Backend)
│   ├── shared/           # Código compartilhado
│   │   ├── database.py   # Conexão com PostgreSQL
│   │   ├── models.py     # SQLAlchemy models
│   │   ├── parser.py     # Parser de battle reports
│   │   └── auth.py       # Autenticação
│   │
│   ├── GetReports/       # Function: GET reports
│   ├── CreateReport/     # Function: POST report
│   ├── DeleteReport/     # Function: DELETE report
│   ├── docs/             # Swagger UI (local only)
│   │
│   ├── host.json
│   ├── requirements.txt
│   └── local.settings.json.example
│
├── iac/            # Infrastructure as Code
│   ├── main.tf          # Recursos principais
│   ├── variables.tf     # Variáveis
│   ├── outputs.tf       # Outputs
│   └── terraform.tfvars.example
│
├── .gitignore
└── README.md
```

## 🧪 Testes

### Backend
```bash
cd api
pytest tests/  # TODO
```

### Frontend
```bash
cd frontend
npm test
```

## 🚀 Workflows CI/CD

### Backend Deploy
- **Trigger**: Push em `api/**` ou workflow manual
- **Passos**: Install → Test → Deploy to Azure Functions

### Frontend Deploy
- **Trigger**: Push em `frontend/**` ou PR
- **Passos**: Install → Test → Build → Deploy to Static Web App

### OpenTofu
- **Plan**: Executa em Pull Requests
- **Apply**: Executa em merge para main

## 📊 Monitoramento

### Application Insights
```bash
# Ver logs em tempo real
az monitor app-insights metrics show \
  --app func-battle-reports-prod \
  --resource-group rg-battle-reports-prod \
  --metric requests/count
```

### Custos Estimados

| Recurso | Tier | Custo Mensal |
|---------|------|--------------|
| Static Web App | Free | $0 |
| Azure Functions | Consumption (1M calls) | $0 |
| PostgreSQL B1ms | 750h (1 ano grátis) | $0 (depois ~$12) |
| **Total Primeiro Ano** | | **$0/mês** |
| **Total Após Free Tier** | | **~$12/mês** |

## 🔒 Segurança

- ✅ API Key authentication
- ✅ CORS configurado apenas para frontend
- ✅ User ID isolation (usuários só veem seus dados)
- ✅ HTTPS obrigatório
- ✅ SSL no PostgreSQL
- ✅ Secrets via environment variables
- ✅ Documentação API apenas em local

## 🐛 Troubleshooting

### Frontend não conecta na API
```bash
# Verificar se a API está rodando
curl http://localhost:7071/api/reports

# Verificar variáveis de ambiente
cat frontend/.env.local
```

### Erro de importação no Python
```bash
# Limpar cache
find api -type d -name "__pycache__" -exec rm -rf {} +

# Reinstalar dependências
cd api
pip install -r requirements.txt --force-reinstall
```

### tofu apply falha
```bash
# Verificar login
az account show

# Ver logs detalhados
export TF_LOG=DEBUG
tofu apply
```

## 📝 Licença

[![LICENSE](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

## 👥 Autor

- Belmiro Neto - [GitHub](https://github.com/belmirocneto)

## 🙏 Agradecimentos

- The Tower game developers
- Azure documentation
- React community
- Anthropic Claude

---

**Nota**: Este projeto não é oficialmente afiliado ao jogo The Tower.