# 📚 Backend - Documentação

> Documentação completa do backend FastAPI do BeeAPI

## 🚀 Início Rápido

| Documento | Descrição | Para quem |
|-----------|-----------|-----------|
| **[README.md](../README.md)** | Setup e visão geral | Novos desenvolvedores |
| **[Poetry Cheat Sheet](POETRY_CHEATSHEET.md)** | Comandos essenciais | Uso diário |
| **[API V2](API_V2.md)** | Endpoints completos | Frontend/Integração |

## 🛠️ Desenvolvimento

### Poetry (Gerenciador de Dependências)

| Arquivo | Descrição | Quando usar |
|---------|-----------|-------------|
| **[Poetry Guide](POETRY_GUIDE.md)** | Tutorial completo do Poetry | Aprender Poetry |
| **[Poetry Cheat Sheet](POETRY_CHEATSHEET.md)** | Comandos rápidos | Referência diária |
| **[Poetry Examples](POETRY_EXAMPLES.md)** | Exemplos práticos BeeAPI | Workflows específicos |
| **[Poetry Setup](POETRY_SETUP.md)** | Configuração no projeto | Setup inicial |

### API e Desenvolvimento

| Arquivo | Descrição | Quando usar |
|---------|-----------|-------------|
| **[API V2](API_V2.md)** | Documentação completa da API | Desenvolvimento frontend |
| **[Migration Guide](MIGRATION_GUIDE.md)** | Migrações de banco | Deploy e atualizações |
| **[Firebase Setup](FIREBASE_SETUP.md)** | Configuração autenticação | Setup de auth |

## 🎯 Workflows por Tarefa

### 🆕 **Setup Inicial**
1. [README.md](../README.md) - Visão geral
2. [Poetry Guide](POETRY_GUIDE.md) - Instalar Poetry
3. [Poetry Examples](POETRY_EXAMPLES.md) - Primeiro comando
4. [API V2](API_V2.md) - Entender endpoints

### 🐛 **Desenvolvimento Diário**
1. [Poetry Cheat Sheet](POETRY_CHEATSHEET.md) - Comandos rápidos
2. [API V2](API_V2.md) - Referência de endpoints
3. [Poetry Examples](POETRY_EXAMPLES.md) - Workflows comuns

### 🚀 **Deploy e Produção**
1. [Migration Guide](MIGRATION_GUIDE.md) - Banco de dados
2. [Firebase Setup](FIREBASE_SETUP.md) - Autenticação
3. [Poetry Setup](POETRY_SETUP.md) - Configurações

### 🔧 **Configuração e Auth**
1. [Firebase Setup](FIREBASE_SETUP.md) - Google OAuth
2. [Migration Guide](MIGRATION_GUIDE.md) - Schema updates
3. [API V2](API_V2.md) - Endpoints de auth

## ⚡ Comandos Rápidos

```bash
# Poetry - Desenvolvimento
cd backend
poetry install              # Setup inicial
poetry shell               # Ativar ambiente
python main.py             # Rodar servidor

# Poetry - Dependências
poetry add pacote          # Adicionar
poetry show               # Listar
poetry update             # Atualizar

# API - Testes
python test_api.py        # Testar endpoints
# Swagger UI: http://localhost:8000/docs
```

## 📁 Estrutura do Backend

```
backend/
├── docs/                          # 📚 Esta documentação
│   ├── README.md                  # Este índice
│   ├── POETRY_*.md               # Documentação Poetry
│   ├── API_V2.md                 # Endpoints da API
│   ├── MIGRATION_GUIDE.md        # Migrações
│   └── FIREBASE_SETUP.md         # Configuração auth
├── controllers/                   # 🎮 Controladores da API
├── models/                        # 📋 Modelos Pydantic
├── middleware/                    # 🔒 Autenticação
├── config/                        # ⚙️ Configurações
├── pyproject.toml                # 📦 Poetry config
├── poetry.lock                   # 🔒 Lock file
├── requirements.txt              # 📜 pip fallback
└── main.py                       # 🚀 Servidor principal
```

## 🔗 Links Externos

- **Swagger UI**: http://localhost:8000/docs
- **Poetry Docs**: https://python-poetry.org/docs/
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Pydantic Docs**: https://docs.pydantic.dev/

## 🏗️ Arquitetura

```
📱 Frontend (React) ←→ 🔥 FastAPI Backend ←→ 🗄️ PostgreSQL + TimescaleDB
                           ↕️
                      🔑 Firebase Auth
```

---

## 💡 Dicas

- **Poetry**: Use `poetry shell` para sessões longas
- **API**: Sempre consulte `/docs` para endpoints atualizados
- **Testes**: Execute `python test_api.py` antes de commit
- **Hot reload**: Use `poetry run uvicorn main:app --reload`

**📝 Contribuindo**: Ao adicionar nova documentação, atualize este README!