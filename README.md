# Briefa - Sistema de Geração de Briefings com IA

Um aplicativo (Web/Mobile) que utiliza Inteligência Artificial Generativa para transformar solicitações informais (áudio, texto solto, anotações manuscritas via OCR) em briefings profissionais, estruturados e validados, prontos para execução por equipes criativas.

## 🚀 Funcionalidades Principais

### Módulo de Entrada de Dados (Input)
- **Chat Natural**: Digite ou fale sua solicitação de forma informal
- **Upload de Arquivos**: Aceita PDFs, imagens de anotações manuscritas (OCR), gravações de áudio
- **Questionário Dinâmico**: IA detecta falta de informação e faz perguntas específicas

### Motor de Inteligência (O Cérebro)
- **Classificação Automática**: Identifica se é briefing Simples, Campanha ou Estratégico
- **Aplicação de Templates**: Seleciona automaticamente o modelo ideal
- **Injeção de Contexto (Tom de Voz)**: Bibliotecas de Tom de Voz pré-configuradas
  - GLPV Humanizado
  - Corporativo B2B
  - Jovem Gen-Z
  - Luxo Premium
- **Validação Técnica**: Sugere especificações automaticamente

### Módulo de Saída (Output)
- **Gerador de Documentos**: Exporta em PDF, DOCX, JSON
- **Checklist de Validação**: Lista do que foi incluído e o que está faltando
- **Sugestão de Referências**: Descrições de referências visuais baseadas no tema

### Gestão e Colaboração
- **Pastas Contextuais**: Briefings relacionados compartilham contexto
- **Histórico de Versões**: Salva rascunhos e permite comparar alterações
- **Fluxo de Aprovação**: Envia para stakeholders aprovar antes da execução
- **Feedback Loop**: Refina a IA com feedback pós-projeto

## 🏗️ Arquitetura

```
backend/
├── main.py           # API FastAPI
├── models.py         # Modelos Pydantic
├── ai_engine.py      # Motor de IA
├── storage.py        # Armazenamento (JSON files)
├── templates.py      # Templates de briefing
└── brand_personas.py # Personas de marca
```

## 🔧 Instalação e Execução

### Pré-requisitos
- Python 3.12+
- pip

### Instalação

```bash
cd backend
pip install -r requirements.txt
```

### Executar o Servidor

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Acessar a API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📖 Uso da API

### 1. Gerar um Briefing

```bash
curl -X POST http://localhost:8000/briefings/generate \
  -H "Content-Type: application/json" \
  -d '{
    "user_input": {
      "text": "Preciso de um post para os 30 anos do hospital, focado em doação, tom emocionante.",
      "input_type": "text",
      "brand_tone": "emotional",
      "brand_persona_id": "glpv_30anos"
    }
  }'
```

### 2. Criar uma Pasta

```bash
curl -X POST "http://localhost:8000/folders?name=GLPV%20-%2030%20Anos&description=Campanha%20de%20celebração"
```

### 3. Salvar um Briefing

```bash
curl -X POST http://localhost:8000/briefings/save \
  -H "Content-Type: application/json" \
  -d '{"title": "...", "description": "...", ...}'
```

### 4. Listar Templates Disponíveis

```bash
curl http://localhost:8000/templates
```

### 5. Listar Personas de Marca

```bash
curl http://localhost:8000/personas
```

## 🎯 Diferenciais Competitivos

1. **Não apenas "gera texto"**: Aplica lógica de projeto (prazos, responsabilidades, especificações técnicas)
2. **Bibliotecas de Tom de Voz**: Pré-configuradas para diferentes perfis de marca
3. **Integração com Fluxos**: Trello, Asana, Jira (simulado na API)
4. **Memória Institucional**: Pastas servem como contexto para briefings similares
5. **Redução de Tempo**: De 45 minutos para 3 minutos na elaboração de briefings

## 📊 Modelos de Complexidade

| Nível | Tipo | Descrição | Template Sugerido |
|-------|------|-----------|-------------------|
| 1 | Tarefa Única | Post único, arte avulsa | Post+Story |
| 2 | Campanha Multi-peça | Múltiplos formatos, eventos | Campanha Completa, Evento Corporativo |
| 3 | Estratégico | Rebrand, posicionamento | Refresh de Marca |

## 👥 Público-Alvo

- Gestores de Marketing e Diretores de Criação
- Agências de Publicidade e Design
- Freelancers que precisam escalar produção de documentação

## 🔐 Segurança e Conformidade

- Criptografia de ponta a ponta (em produção)
- Conformidade com LGPD
- Dados sensíveis de campanhas não lançadas protegidas

## 📈 Roadmap

- [ ] Integração real com OpenAI/Anthropic APIs
- [ ] OCR para anotações manuscritas
- [ ] Transcrição de áudio (Speech-to-Text)
- [ ] Export PDF/DOCX formatado
- [ ] Integrações reais: Trello, Asana, Jira, Slack
- [ ] Autenticação e autorização de usuários
- [ ] Banco de dados PostgreSQL/MongoDB
- [ ] Frontend React/Vue.js

## 📝 License

MIT License
