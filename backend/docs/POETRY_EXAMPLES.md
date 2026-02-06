# 🐝 BeeAPI - Exemplos Práticos com Poetry

## 🚀 Setup Inicial (Uma vez só)

```bash
# 1. Clonar projeto
git clone https://github.com/Iuri1012/beeApi.git
cd beeApi/backend

# 2. Verificar se Poetry está instalado
poetry --version

# 3. Instalar dependências
poetry install

# 4. Verificar ambiente criado
poetry env info
```

## 💻 Desenvolvimento Diário

### **Opção 1: Ativar ambiente primeiro**
```bash
cd backend
poetry shell                    # ✅ Ativar ambiente (uma vez por sessão)
python main.py                  # 🚀 Rodar backend
python test_api.py              # 🧪 Rodar testes
exit                            # 🚪 Sair do ambiente
```

### **Opção 2: Comandos únicos**
```bash
cd backend
poetry run python main.py       # 🚀 Rodar backend
poetry run python test_api.py   # 🧪 Rodar testes
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8000  # 🔥 Hot reload
```

## 🔧 Adicionando Dependências

### **Dependências de Produção**
```bash
# Adicionar Redis para cache
poetry add redis

# Adicionar Pandas para análise
poetry add pandas

# Versão específica
poetry add requests==2.31.0

# Range de versões  
poetry add "fastapi>=0.100,<1.0"
```

### **Dependências de Desenvolvimento**
```bash
# Ferramentas de teste
poetry add --group dev pytest-cov
poetry add --group dev pytest-mock

# Formatação e linting
poetry add --group dev black
poetry add --group dev flake8
poetry add --group dev isort

# Documentação
poetry add --group dev sphinx
```

## 📊 Cenários Específicos BeeAPI

### **🔍 Debugging**
```bash
# Ver todas as dependências
poetry show

# Ver dependências em árvore
poetry show --tree

# Info do ambiente virtual
poetry env info

# Verificar conflitos
poetry check
```

### **🧪 Testes**
```bash
# Rodar testes básicos
poetry run python test_api.py

# Com pytest (se instalado)
poetry add --group dev pytest
poetry run pytest

# Com coverage
poetry add --group dev pytest-cov
poetry run pytest --cov=. --cov-report=html
```

### **🚀 Deploy**
```bash
# Exportar para requirements.txt (para Docker)
poetry export -f requirements.txt --output requirements.txt

# Apenas produção (sem dev)
poetry export -f requirements.txt --output requirements.txt --without dev

# Com hashes para segurança
poetry export -f requirements.txt --output requirements.txt --without dev --with-credentials
```

## 🏗️ Workflows Completos

### **🆕 Nova Feature**
```bash
# 1. Ativar ambiente
poetry shell

# 2. Trabalhar no código
# ... editar arquivos ...

# 3. Adicionar dependência se necessário
poetry add nova-dependencia

# 4. Testar
python test_api.py

# 5. Commit (inclui poetry.lock!)
git add .
git commit -m "Add nova feature"
```

### **🔄 Após git pull**
```bash
# Instalar novas dependências
poetry install

# Se mudou Python
poetry env remove python
poetry install
```

### **🐛 Resolver Problemas**
```bash
# Limpar cache
poetry cache clear pypi --all

# Recriar ambiente
poetry env remove python
poetry install

# Update de tudo
poetry update
```

## 📱 APIs e Endpoints

### **Testar Endpoints Específicos**
```bash
# Rodar backend em desenvolvimento
poetry run uvicorn main:app --reload

# Em outro terminal, testar API
poetry run python -c "
import requests
response = requests.get('http://localhost:8000/health')
print(response.json())
"
```

### **Teste do Endpoint de Update Events**
```bash
# Rodar backend
poetry shell
python main.py

# Em outro terminal, testar PUT /events/{id}
curl -X PUT http://localhost:8000/events/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-token" \
  -d '{"description": "Updated event description"}'
```

## 🐳 Docker + Poetry

### **Dockerfile com Poetry**
```dockerfile
FROM python:3.9-slim

# Instalar Poetry
RUN pip install poetry

# Copiar arquivos de configuração
COPY pyproject.toml poetry.lock ./

# Instalar dependências
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copiar código
COPY . .

CMD ["python", "main.py"]
```

### **Build e Run**
```bash
# Build
docker build -t beeapi .

# Run
docker run -p 8000:8000 beeapi
```

## 🎯 Comparação Rápida

| Situação | Comando pip | Comando Poetry |
|----------|-------------|----------------|
| **Setup projeto** | `pip install -r requirements.txt` | `poetry install` |
| **Rodar script** | `python main.py` | `poetry run python main.py` |
| **Adicionar dep** | `pip install redis` + editar requirements.txt | `poetry add redis` |
| **Ambiente virtual** | `python -m venv venv && source venv/bin/activate` | `poetry shell` |
| **Ver dependências** | `pip list` | `poetry show` |
| **Update** | `pip install --upgrade -r requirements.txt` | `poetry update` |

## 💡 Dicas Específicas BeeAPI

1. **Sempre commitar `poetry.lock`** - garante reprodutibilidade
2. **Use `poetry shell`** para sessões longas de desenvolvimento  
3. **Use `poetry run`** para comandos únicos
4. **Mantenha `requirements.txt`** para compatibilidade Docker
5. **Teste endpoints** com `poetry run python test_api.py`

---

## 🔗 Próximos Passos

- **Explorar**: [Poetry Guide Completo](POETRY_GUIDE.md)
- **Referência**: [Poetry Cheat Sheet](POETRY_CHEATSHEET.md) 
- **APIs**: [Documentação da API](API_V2.md)
- **Deploy**: [Guia de Migração](MIGRATION_GUIDE.md)