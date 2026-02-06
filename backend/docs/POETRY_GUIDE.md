# 📖 Poetry - Guia de Comandos Básicos

> **Poetry** é o gerenciador moderno de dependências para Python, similar ao npm para Node.js

## 🚀 Instalação do Poetry

```bash
# macOS/Linux usando Homebrew (recomendado)
brew install poetry

# Ou usando curl
curl -sSL https://install.python-poetry.org | python3 -

# Verificar instalação
poetry --version
```

## 📁 Estrutura de Projeto Poetry

```
projeto/
├── pyproject.toml          # Configuração principal (como package.json)
├── poetry.lock            # Lock file (como package-lock.json)
├── README.md              # Documentação
└── src/                   # Código fonte
    └── main.py
```

## 🎯 Comandos Essenciais

### **Inicialização de Projeto**

```bash
# Criar novo projeto
poetry new meu-projeto

# Inicializar em projeto existente
poetry init

# Inicializar sem interação
poetry init --no-interaction --name meu-app --version 1.0.0
```

### **Gerenciamento de Dependências**

```bash
# Instalar todas as dependências
poetry install

# Adicionar dependência de produção
poetry add fastapi
poetry add requests==2.31.0    # versão específica
poetry add "django>=4.0,<5.0"  # range de versões

# Adicionar dependência de desenvolvimento
poetry add --group dev pytest
poetry add --group dev black flake8

# Remover dependência
poetry remove requests

# Atualizar dependências
poetry update               # todas
poetry update requests      # específica

# Ver dependências instaladas
poetry show                 # lista completa
poetry show requests        # detalhes de uma específica
poetry show --tree          # árvore de dependências
```

### **Ambiente Virtual**

```bash
# Ver informações do ambiente
poetry env info

# Ativar shell do ambiente virtual
poetry shell

# Sair do ambiente
exit

# Executar comando no ambiente (sem ativar)
poetry run python main.py
poetry run pytest
poetry run black .

# Remover ambiente virtual
poetry env remove python
```

### **Scripts e Execução**

```bash
# No BeeAPI, exemplos de comandos:
cd backend

# Executar servidor
poetry run python main.py
poetry run uvicorn main:app --reload

# Executar testes
poetry run python test_api.py
poetry run pytest

# Executar formatação
poetry run black .
poetry run flake8
```

## 🔧 Arquivo pyproject.toml Explicado

```toml
[tool.poetry]
name = "beeapi"                                    # Nome do projeto
version = "2.0.0"                                 # Versão
description = "IoT Beehive Monitoring API"        # Descrição
authors = ["Seu Nome <email@exemplo.com>"]        # Autores
readme = "README.md"                               # Arquivo README
package-mode = false                               # Não empacotar como biblioteca

[tool.poetry.dependencies]                        # Dependências de produção
python = "^3.9,<3.14"                            # Versão Python
fastapi = "0.109.1"                              # Versão específica
uvicorn = {extras = ["standard"], version = "0.27.0"}  # Com extras
requests = "^2.31.0"                             # Versão compatível

[tool.poetry.group.dev.dependencies]             # Dependências de desenvolvimento
pytest = "^7.0.0"
black = "^23.0.0"
flake8 = "^6.0.0"

[tool.poetry.scripts]                            # Scripts customizados (opcional)
dev = "uvicorn main:app --reload"
test = "pytest tests/"

[build-system]                                   # Sistema de build
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 📋 Comandos do BeeAPI

### **Setup Inicial**

```bash
# Clonar projeto
git clone https://github.com/Iuri1012/beeApi.git
cd beeApi/backend

# Instalar dependências
poetry install

# Verificar ambiente
poetry env info
```

### **Desenvolvimento Diário**

```bash
# Ativar ambiente
poetry shell

# Executar backend
python main.py
# ou sem ativar ambiente:
poetry run python main.py

# Executar com hot reload
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### **Gerenciamento de Dependências**

```bash
# Adicionar nova dependência
poetry add httpx               # para produção
poetry add --group dev pytest # para desenvolvimento

# Ver o que está instalado
poetry show

# Atualizar tudo
poetry update
```

## 🆚 Poetry vs Outros Gerenciadores

| Ação | pip | Poetry | npm |
|------|-----|---------|-----|
| **Arquivo config** | `requirements.txt` | `pyproject.toml` | `package.json` |
| **Lock file** | ❌ | `poetry.lock` | `package-lock.json` |
| **Instalar deps** | `pip install -r requirements.txt` | `poetry install` | `npm install` |
| **Adicionar dep** | `pip install requests` | `poetry add requests` | `npm install express` |
| **Ambiente virtual** | `python -m venv venv` | `poetry shell` | - |
| **Executar comando** | `python main.py` | `poetry run python main.py` | `npm run dev` |
| **Ver deps** | `pip list` | `poetry show` | `npm list` |

## ⚡ Dicas e Truques

### **Configuração Global**

```bash
# Configurar Poetry para criar venv no projeto
poetry config virtualenvs.in-project true

# Ver configurações
poetry config --list

# Configurar repositório privado
poetry config repositories.meu-repo https://meu-repo.com/simple/
```

### **Workflows Comuns**

```bash
# Workflow típico de desenvolvimento
poetry shell                   # Ativar ambiente
poetry add nova-dependencia    # Adicionar o que precisar
git add pyproject.toml poetry.lock
git commit -m "Add nova-dependencia"

# Após git pull
poetry install                 # Instalar novas dependências

# Deploy/Produção
poetry export -f requirements.txt --output requirements.txt
# ou usar poetry diretamente no container
```

### **Resolução de Problemas**

```bash
# Limpar cache
poetry cache clear pypi --all

# Recriar ambiente
poetry env remove python
poetry install

# Debug de dependências
poetry show --tree
poetry check

# Forçar reinstalação
poetry install --no-cache
```

## 🎯 Comandos Mais Usados (Cheat Sheet)

```bash
# Setup
poetry install

# Ambiente
poetry shell
poetry env info

# Dependências  
poetry add pacote
poetry remove pacote
poetry show

# Execução
poetry run python main.py
poetry run pytest

# Manutenção
poetry update
poetry check
```

## 📝 Exemplo Prático - BeeAPI

```bash
# 1. Setup inicial
cd /Users/iurisoares/repos/beeApi/backend
poetry install

# 2. Desenvolvimento
poetry shell
python main.py

# 3. Adicionar dependência
poetry add redis

# 4. Executar testes
poetry run python test_api.py

# 5. Deploy
poetry export -f requirements.txt --output requirements.txt
```

---

## 🔗 Recursos Adicionais

- **Documentação oficial**: https://python-poetry.org/docs/
- **Arquivo pyproject.toml**: https://python-poetry.org/docs/pyproject/
- **Configurações**: https://python-poetry.org/docs/configuration/
- **Scripts customizados**: https://python-poetry.org/docs/pyproject/#scripts

**💡 Dica**: Use `poetry shell` para ativar o ambiente e trabalhar normalmente, ou `poetry run` para comandos únicos!