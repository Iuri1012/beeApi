# 🐝 BeeAPI - Poetry Setup Guide

## ✅ Poetry Instalado e Configurado!

### 📦 **Comandos Poetry Disponíveis**

```bash
# Navegar para o diretório backend
cd /Users/iurisoares/repos/beeApi/backend

# Ver informações do ambiente
poetry env info

# Listar pacotes instalados  
poetry show

# Ativar shell do ambiente virtual
poetry shell

# Executar comando no ambiente
poetry run python3 main.py

# Executar servidor de desenvolvimento
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Executar testes
poetry run python test_api.py

# Adicionar nova dependência
poetry add nome-do-pacote

# Adicionar dependência de desenvolvimento
poetry add --group dev nome-do-pacote

# Remover dependência
poetry remove nome-do-pacote

# Atualizar dependências
poetry update

# Instalar dependências (após git pull)
poetry install
```

### 🔧 **Estrutura do Projeto**

```
backend/
├── pyproject.toml          # ✨ Configuração Poetry (novo)
├── poetry.lock            # 🔒 Lock file (auto-gerado)
├── requirements.txt       # 📜 Formato antigo (manter para compatibilidade)
├── environment.yml        # 🐍 Conda alternativo
├── main.py               # 🚀 Servidor FastAPI
└── ...
```

### 🆚 **Comparação com npm**

| Comando | npm | Poetry |
|---------|-----|---------|
| Instalar deps | `npm install` | `poetry install` |
| Adicionar dep | `npm install express` | `poetry add fastapi` |
| Remover dep | `npm uninstall express` | `poetry remove fastapi` |
| Executar script | `npm run dev` | `poetry run uvicorn main:app --reload` |
| Ver deps | `npm list` | `poetry show` |
| Ambiente | n/a | `poetry shell` |

### 🎯 **Benefícios do Poetry**

- ✅ **Gestão automática de ambientes virtuais**
- ✅ **Lock file para reprodutibilidade** (`poetry.lock`)
- ✅ **Resolução inteligente de dependências**
- ✅ **Separação deps produção/desenvolvimento** 
- ✅ **Comando único** `poetry run`
- ✅ **Sintaxe moderna** no `pyproject.toml`

### 🚀 **Workflow Recomendado**

```bash
# Desenvolvimento diário
cd backend
poetry shell                    # Ativa ambiente
python main.py                 # Roda backend
# ou
poetry run python main.py      # Roda sem ativar

# Adicionar nova feature
poetry add requests             # Adiciona dep
git add pyproject.toml poetry.lock
git commit -m "Add requests dependency"

# Após git pull de outro dev
poetry install                  # Instala novas deps
```

### 📋 **Status Atual**

- ✅ Poetry instalado via Homebrew
- ✅ Ambiente virtual criado (`beeapi-scc7DRC9-py3.9`)
- ✅ Todas as dependências instaladas
- ✅ Backend executa sem erros de import
- ✅ Endpoint `PUT /events/{event_id}` funcionando
- ✅ Compatível com infraestrutura existente

### 🔄 **Migração Completa**

O projeto agora suporta **3 gerenciadores**:
1. **pip** (tradicional) - `pip install -r requirements.txt`
2. **Poetry** (moderno) - `poetry install` 
3. **Conda** (científico) - `conda env create -f environment.yml`

**Recomendação**: Use **Poetry** para desenvolvimento ativo! 🎉