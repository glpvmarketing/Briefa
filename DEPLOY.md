# 🚀 Briefa - Deploy Guide

## Como Fazer Deploy Público

### Opção 1: Render (Recomendado - Mais Fácil)

1. **Acesse** https://render.com e crie uma conta gratuita

2. **Crie um novo Web Service:**
   - Clique em "New +" → "Web Service"
   - Conecte seu repositório GitHub
   - Selecione o repositório do Briefa

3. **Configure o Deploy:**
   ```
   Name: briefa-api
   Region: São Paulo (ou mais próximo)
   Branch: main (ou sua branch)
   Root Directory: Deixe em branco
   Runtime: Python 3
   Build Command: pip install -r backend/requirements.txt
   Start Command: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```

4. **Plano Gratuito:**
   - Selecione "Free"
   - Instância: 512MB RAM

5. **Clique em "Create Web Service"**

6. **Aguarde o deploy** (~2-3 minutos)

7. **Acesse sua API:**
   - URL: `https://briefa-api.onrender.com`
   - Swagger: `https://briefa-api.onrender.com/docs`

---

### Opção 2: Railway

1. **Acesse** https://railway.app e crie conta

2. **Deploy from GitHub:**
   - Clique em "New Project"
   - "Deploy from GitHub repo"
   - Selecione seu repositório

3. **Configure as variáveis de ambiente:**
   ```
   PORT: 8080
   ```

4. **Adicione no railway.toml:**
   ```toml
   [build]
   builder = "NIXPACKS"

   [deploy]
   startCommand = "uvicorn backend.main:app --host 0.0.0.0 --port $PORT"
   ```

---

### Opção 3: Hugging Face Spaces

1. **Acesse** https://huggingface.co/spaces

2. **Create New Space:**
   - Space name: briefa-api
   - License: MIT
   - SDK: Docker

3. **Crie um Dockerfile** no repositório:
   ```dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   COPY . .
   CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
   ```

4. **Push o código** para o Space

5. **Acesse:** `https://huggingface.co/spaces/seu-usuario/briefa-api`

---

### Opção 4: Rodar Localmente (Para Testes)

```bash
# Clone seu repositório
git clone https://github.com/SEU-USUARIO/briefa.git
cd briefa

# Instale dependências
pip install -r backend/requirements.txt

# Rode o servidor
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

# Acesse:
# http://localhost:8000
# http://localhost:8000/docs
```

---

## Após o Deploy

### Teste a API:

1. **Acesse o Swagger UI:**
   ```
   https://SEU-DOMINIO.com/docs
   ```

2. **Teste os endpoints:**
   - `/api/personas/` - Lista personas de marca
   - `/api/templates/` - Lista templates
   - `/api/folders/` - Gerencia pastas
   - `/api/briefings/generate/` - Gera briefing com IA

3. **Exemplo de uso:**
   ```bash
   # Criar pasta
   curl -X POST https://SEU-DOMINIO.com/api/folders/ \
     -H "Content-Type: application/json" \
     -d '{"name": "Campanha 30 Anos", "brand_persona_id": 1}'

   # Gerar briefing
   curl -X POST https://SEU-DOMINIO.com/api/briefings/generate/ \
     -H "Content-Type: application/json" \
     -d '{
       "folder_id": "ID_DA_PASTA",
       "input_text": "Post para 30 anos do hospital, tom emocionante",
       "template_id": 1
     }'
   ```

---

## Solução de Problemas

### Erro: "Module not found"
- Verifique se o `requirements.txt` está correto
- Reinstale: `pip install -r backend/requirements.txt`

### Erro: "Port already in use"
- Mude a porta: `--port 8080`

### Deploy falhando no Render
- Verifique os logs em "Logs" tab
- Confirme que o `Procfile` está na raiz

### API não responde
- Aguarde 2-3 minutos após deploy (serviços free dormem)
- Primeiro request pode demorar ~30s (cold start)

---

## Próximos Passos

1. ✅ Fazer deploy em um dos serviços acima
2. ✅ Testar todos os endpoints via Swagger
3. ✅ Compartilhar URL pública com sua equipe
4. 🔄 Opcional: Criar frontend React/Vue
5. 🔄 Opcional: Adicionar autenticação
6. 🔄 Opcional: Integrar com Trello/Asana

---

## URLs Úteis

- **Render:** https://render.com
- **Railway:** https://railway.app
- **Hugging Face:** https://huggingface.co/spaces
- **FastAPI Docs:** https://fastapi.tiangolo.com
