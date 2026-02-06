# 🚀 Poetry - Cheat Sheet Rápido

## ⚡ Comandos Essenciais

```bash
# SETUP
poetry install              # Instalar dependências
poetry shell               # Ativar ambiente virtual

# DEPENDÊNCIAS
poetry add fastapi         # Adicionar produção
poetry add --group dev pytest  # Adicionar desenvolvimento
poetry remove requests     # Remover
poetry show                # Listar instaladas
poetry update              # Atualizar todas

# EXECUÇÃO
poetry run python main.py  # Executar no ambiente
poetry run pytest         # Rodar testes

# AMBIENTE
poetry env info            # Info do ambiente
poetry env remove python  # Remover ambiente

# ÚTEIS
poetry check              # Verificar consistência
poetry config --list     # Ver configurações
```

## 📁 Estrutura Básica

```
projeto/
├── pyproject.toml     # ← Configuração principal
├── poetry.lock       # ← Lock file (auto-gerado)
└── src/main.py
```

## 🎯 BeeAPI - Comandos Práticos

```bash
# Navegar para o projeto
cd /Users/iurisoares/repos/beeApi/backend

# Setup inicial (uma vez)
poetry install

# Desenvolvimento diário
poetry shell                                    # Ativar ambiente
python main.py                                 # Rodar backend
# ou
poetry run python main.py                     # Rodar sem ativar

# Servidor com hot reload
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Testes
poetry run python test_api.py

# Adicionar dependências
poetry add redis                               # Produção
poetry add --group dev black                  # Desenvolvimento

# Ver o que está instalado
poetry show
```

## 🔧 pyproject.toml - Template

```toml
[tool.poetry]
name = "meu-app"
version = "1.0.0"
description = "Minha aplicação"
authors = ["Nome <email@exemplo.com>"]

[tool.poetry.dependencies]
python = "^3.9"
fastapi = "^0.109.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 💡 Dicas Rápidas

- **`poetry shell`** = ambiente ativo permanente
- **`poetry run`** = comando único no ambiente  
- **`poetry.lock`** = sempre commitar no git
- **`--group dev`** = dependências só para desenvolvimento
- **`poetry check`** = verificar se tudo está OK

---
**📖 Guia completo**: [POETRY_GUIDE.md](POETRY_GUIDE.md)