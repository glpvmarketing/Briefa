# Briefa - Gerador de Briefings com IA

Sistema completo para transformação de solicitações informais em briefings profissionais estruturados usando Inteligência Artificial Generativa.

## 🚀 Funcionalidades

- **Entrada Natural**: Digite, fale ou faça upload de anotações
- **IA Inteligente**: Classifica complexidade e aplica templates automaticamente
- **Personas de Marca**: GLPV, B2B Corporativo, Gen-Z, Luxury
- **Templates Profissionais**: 5 modelos prontos para diferentes cenários
- **Especificações Técnicas**: Dimensões, formatos e requisitos automáticos
- **Memória Institucional**: Pastas contextuais aprendem com projetos anteriores
- **Validação Automática**: Checklists inteligentes
- **Fluxo de Aprovação**: Stakeholders podem revisar antes da execução

## 🎯 Como Usar

### Opção 1: Abrir Localmente (Recomendado)

1. **Abra o arquivo `frontend/index.html` diretamente no seu navegador**:
   - Navegue até a pasta do projeto
   - Clique duas vezes em `frontend/index.html`
   - O app abrirá no seu navegador

2. **Ou inicie o servidor backend e acesse pelo navegador**:
   ```bash
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```
   
   Acesse: **http://localhost:8000**

### Opção 2: Documentação da API

Com o servidor rodando, acesse:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 📁 Estrutura do Projeto

```
/workspace/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── models.py            # Modelos de dados
│   ├── ai_engine.py         # Motor de IA
│   ├── storage.py           # Armazenamento local
│   ├── templates.py         # Templates de briefing
│   ├── brand_personas.py    # Personas de marca
│   └── requirements.txt     # Dependências
├── frontend/
│   └── index.html           # Interface web completa
├── data/                    # Dados armazenados
│   ├── briefings/
│   ├── folders/
│   └── personas/
└── README.md
```

## 🔧 Instalação

### Requisitos
- Python 3.9+
- Navegador web moderno (Chrome, Firefox, Edge)

### Passos

1. **Instale as dependências**:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Inicie o servidor**:
   ```bash
   cd backend
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. **Acesse a aplicação**:
   - Frontend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## 🎨 Uso da Aplicação

### 1. Criar uma Pasta
- Vá na aba "Pastas"
- Digite o nome do projeto/cliente
- Clique em "Criar"

### 2. Selecionar Persona de Marca
- Escolha entre: GLPV, B2B, Gen-Z, ou Luxury
- Cada persona tem tom de voz e diretrizes específicas

### 3. Descrever o Projeto
Exemplo:
```
Preciso de um post para os 30 anos do hospital, 
focado em doação, tom emocionante. Data: 03/06. 
Deliverables: posts, stories, thumb.
```

### 4. Gerar Briefing
- Clique em "Gerar Briefing"
- A IA processa em segundos
- Visualize o resultado estruturado

### 5. Ações Disponíveis
- 💾 **Salvar**: Armazena na pasta selecionada
- 🔄 **Gerar Outro**: Cria nova versão
- 📥 **Exportar**: Baixa o briefing
- 🗑️ **Descartar**: Remove o rascunho

## 📊 Endpoints da API

### Pastas
- `GET /folders` - Listar pastas
- `POST /folders` - Criar pasta
- `DELETE /folders/{id}` - Excluir pasta
- `GET /folders/{id}` - Detalhes da pasta

### Personas
- `GET /personas` - Listar personas
- `GET /personas/{id}` - Detalhes da persona

### Briefings
- `POST /generate-briefing` - Gerar briefing com IA
- `POST /briefings` - Salvar briefing
- `GET /briefings` - Listar briefings
- `GET /briefings/{id}` - Detalhes do briefing
- `PUT /briefings/{id}` - Atualizar briefing
- `DELETE /briefings/{id}` - Excluir briefing

### Templates
- `GET /templates` - Listar templates
- `GET /templates/{id}` - Detalhes do template

## 🤖 Motor de IA

O sistema classifica automaticamente:

### Níveis de Complexidade
- **Nível 1 (Simples)**: Tarefa única (ex: post único)
- **Nível 2 (Campanha)**: Múltiplas peças e formatos
- **Nível 3 (Estratégico)**: Objetivos de negócio + KPIs

### Templates Disponíveis
1. **Post+Story**: Redes sociais básicas
2. **Campanha Completa**: Multi-peças e canais
3. **Evento Corporativo**: Lançamentos e celebrações
4. **Refresh de Marca**: Reposicionamento
5. **Produção de Vídeo**: Conteúdo audiovisual

## 🔒 Segurança

- Dados armazenados localmente
- Sem envio para servidores externos
- Pronto para adequação LGPD

## 🛠️ Tecnologias

- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript puro
- **Armazenamento**: JSON files (local)
- **IA**: Lógica heurística + processamento de linguagem natural

## 📝 Exemplo de Briefing Gerado

Um briefing completo inclui:
- ✅ Nome e objetivo do projeto
- ✅ Público-alvo definido
- ✅ Tom de voz da marca
- ✅ Lista de deliverables
- ✅ Especificações técnicas
- ✅ Cronograma sugerido
- ✅ Checklist de validação
- ✅ Observações e referências

## 🚀 Próximos Passos (Deploy Público)

Para disponibilizar online:

1. **Render/Railway**:
   - Crie conta em render.com ou railway.app
   - Conecte seu repositório GitHub
   - Configure:
     - Build: `pip install -r backend/requirements.txt`
     - Start: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

2. **Hugging Face Spaces**:
   - Crie um Space tipo "Docker"
   - Adicione Dockerfile incluso
   - Deploy automático

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique se o backend está rodando
2. Confira o console do navegador (F12)
3. Teste a API em http://localhost:8000/docs

---

**Briefa** - Transformando ideias em briefings profissionais em segundos! ⚡
