# 📚 BeeAPI - Central de Documentação

> Documentação completa e organizada do projeto BeeAPI

## 🗂️ Organização

### 📖 **[Guias](guides/)**
| Arquivo | Descrição | Para quem |
|---------|-----------|-----------|
| **[QUICKSTART.md](guides/QUICKSTART.md)** | Setup completo em 5 minutos | Novos usuários |
| **[CONTRIBUTING.md](guides/CONTRIBUTING.md)** | Como contribuir | Colaboradores |
| **[QUICK_REFERENCE.md](guides/QUICK_REFERENCE.md)** | Referência rápida | Uso diário |
| **[TESTING.md](guides/TESTING.md)** | Como executar testes | QA e desenvolvimento |
| **[API.md](guides/API.md)** | Documentação da API geral | Integrações |
| **[example_client.py](guides/example_client.py)** | Cliente de exemplo | Desenvolvimento |

### 🏗️ **[Arquitetura](architecture/)**  
| Arquivo | Descrição | Para quem |
|---------|-----------|-----------|
| **[DATABASE_ARCHITECTURE.md](architecture/DATABASE_ARCHITECTURE.md)** | Design dos bancos PostgreSQL/TimescaleDB | DevOps/DBA |
| **[OVERVIEW.md](architecture/OVERVIEW.md)** | Arquitetura completa do sistema | Desenvolvedores |

### 📋 **[Resumos](summaries/)**
| Arquivo | Descrição | Para quem |
|---------|-----------|-----------|
| **[PROJECT_SUMMARY.md](summaries/PROJECT_SUMMARY.md)** | Resumo executivo | Stakeholders |
| **[REFACTORING_COMPLETE.md](summaries/REFACTORING_COMPLETE.md)** | Resumo do refactoring v2.0 | Time técnico |
| **[UPDATE_SUMMARY.md](summaries/UPDATE_SUMMARY.md)** | Resumo de atualizações | Acompanhamento |

### � **[Changelogs](changelogs/)**
| Arquivo | Descrição | Para quem |
|---------|-----------|-----------|
| **[CHANGELOG.md](changelogs/CHANGELOG.md)** | Histórico de mudanças | Todos |

### 🔥 **[Backend](../backend/docs/)**
| Seção | Descrição | Para quem |
|-------|-----------|-----------|
| **[Índice Backend](../backend/docs/README.md)** | Docs específicas do backend | Backend devs |
| **[Poetry Guides](../backend/docs/POETRY_GUIDE.md)** | Gerenciamento de dependências | Python devs |
| **[API V2](../backend/docs/API_V2.md)** | Endpoints detalhados | Frontend devs |

## 🎯 Workflows por Cenário

### 🆕 **Primeiro Acesso**
1. [README.md](../README.md) - Visão geral
2. [QUICKSTART.md](guides/QUICKSTART.md) - Setup rápido
3. [OVERVIEW.md](architecture/OVERVIEW.md) - Entender arquitetura

### 🛠️ **Desenvolvimento Backend** 
1. [Backend Docs](../backend/docs/README.md) - Hub do backend
2. [Poetry Guide](../backend/docs/POETRY_GUIDE.md) - Setup ambiente
3. [API V2](../backend/docs/API_V2.md) - Endpoints

### 🎨 **Desenvolvimento Frontend**
1. [API.md](guides/API.md) - API geral
2. [API V2](../backend/docs/API_V2.md) - Endpoints específicos
3. [example_client.py](guides/example_client.py) - Exemplo de uso

### 📊 **Data Science / Analytics**
1. [DATABASE_ARCHITECTURE.md](architecture/DATABASE_ARCHITECTURE.md) - Estrutura dados
2. [OVERVIEW.md](architecture/OVERVIEW.md) - Fluxo de telemetria

### 🚀 **Deploy / Produção**
1. [Backend Migration](../backend/docs/MIGRATION_GUIDE.md) - Deploy backend
2. [DATABASE_ARCHITECTURE.md](architecture/DATABASE_ARCHITECTURE.md) - Setup bancos

### � **Acompanhamento Projeto**
1. [PROJECT_SUMMARY.md](summaries/PROJECT_SUMMARY.md) - Status geral
2. [CHANGELOG.md](changelogs/CHANGELOG.md) - O que mudou
3. [REFACTORING_COMPLETE.md](summaries/REFACTORING_COMPLETE.md) - Refactoring v2.0

## 🔧 Por Componente

### Backend FastAPI
- **[Documentação Completa](../backend/docs/README.md)**
- Poetry, API, Migrações, Firebase

### Frontend React
- **[Web README](../web/README.md)**
- Dashboard React

### Telemetria IoT
- **[Firmware README](../firmware/README.md)**
- **[Telemetry README](../telemetry/README.md)** 
- **[TimescaleDB](../timeseries/README.md)**

### Gateway & Infraestrutura
- **[Gateway README](../gateway/README.md)**
- **[Docker](../docker/)**

## ⚡ Links Rápidos

- **🚀 Começar**: [QUICKSTART.md](guides/QUICKSTART.md)
- **🔥 Backend**: [Backend Docs](../backend/docs/README.md)
- **📊 Dados**: [DATABASE_ARCHITECTURE.md](architecture/DATABASE_ARCHITECTURE.md)
- **🌐 API**: [API V2](../backend/docs/API_V2.md)
- **📖 Contrib**: [CONTRIBUTING.md](guides/CONTRIBUTING.md)

---

## 📁 Estrutura Completa

```
docs/
├── README.md                   # Este índice
├── architecture/               # 🏗️ Arquitetura e design
│   ├── DATABASE_ARCHITECTURE.md
│   └── OVERVIEW.md
├── guides/                     # 📖 Guias e tutoriais
│   ├── QUICKSTART.md
│   ├── CONTRIBUTING.md
│   ├── QUICK_REFERENCE.md
│   ├── TESTING.md
│   ├── API.md
│   └── example_client.py
├── summaries/                  # 📋 Resumos executivos
│   ├── PROJECT_SUMMARY.md
│   ├── REFACTORING_COMPLETE.md
│   └── UPDATE_SUMMARY.md
└── changelogs/                 # 📝 Histórico de mudanças
    └── CHANGELOG.md
```

**🎯 Navegue pela estrutura ou use os workflows para encontrar rapidamente o que precisa!**
└─────────────┘        │
                       ▼
┌─────────────┐   ┌──────────┐   ┌─────────────┐
│  Firmware   │   │ Mosquitto│   │ Telemetry   │
│  Simulator  │──▶│  (MQTT)  │──▶│  Consumer   │
└─────────────┘   └──────────┘   └──────┬──────┘
                                         │
                                         ▼
                  ┌─────────────────────────┐
                  │   PostgreSQL +          │
                  │   TimescaleDB           │
                  └───────────┬─────────────┘
                              │
                              ▼
┌─────────────┐   ┌──────────────────┐
│   React     │   │  FastAPI         │
│   Web UI    │◀──│  Backend         │
└─────────────┘   └──────────────────┘
```

## Data Flow

1. **Device → MQTT**: Beehive devices publish telemetry to MQTT topics
2. **MQTT → Consumer**: Telemetry consumer subscribes and receives messages
3. **Consumer → Database**: Consumer stores data in TimescaleDB hypertable
4. **Web → Backend**: React app fetches data via REST API
5. **Backend → Web**: WebSocket streams real-time updates

## Components

### Firmware Simulator
- Simulates beehive IoT devices
- Publishes realistic telemetry data
- Configurable interval and device ID

### MQTT Broker (Mosquitto)
- Message broker for device communication
- Topic structure: `beehive/{device_id}/telemetry`

### Telemetry Consumer
- Python service subscribing to MQTT
- Validates and stores data in database
- Handles device registration checks

### Backend API (FastAPI)
- RESTful API for device and data management
- WebSocket support for real-time updates
- Async database connections

### TimescaleDB
- Time-series database for telemetry
- Hypertable for efficient time-based queries
- Continuous aggregates for analytics

### Web Dashboard
- React-based UI
- Real-time charts and metrics
- WebSocket integration for live data

## API Reference

See [API.md](API.md) for detailed endpoint documentation.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for production deployment guide.
