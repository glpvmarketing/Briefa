"""
Briefa API - Sistema de Geração de Briefings com IA
API REST para criação, gestão e exportação de briefings profissionais
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Optional, Dict, Any
import uuid
import os

from models import (
    Briefing, Folder, UserInput, GenerationRequest, GenerationResponse,
    BrandTone, ComplexityLevel, ApprovalRequest, ApprovalResponse
)
from ai_engine import ai_engine
from storage import storage
from templates import get_all_templates, get_template
from brand_personas import get_all_personas, get_persona, get_tone_guidelines

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="Briefa API",
    description="Sistema de geração de briefings profissionais com Inteligência Artificial",
    version="1.0.0"
)

# Configura CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# === Health Check ===

@app.get("/")
async def root():
    """Endpoint de saúde da API"""
    return {
        "service": "Briefa API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Verifica se o serviço está saudável"""
    return {"status": "healthy"}


# === Templates ===

@app.get("/templates", tags=["Templates"])
async def list_templates():
    """Lista todos os templates disponíveis"""
    return {"templates": get_all_templates()}


@app.get("/templates/{template_id}", tags=["Templates"])
async def get_template_by_id(template_id: str):
    """Retorna um template específico"""
    template = get_template(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template não encontrado")
    return template


# === Brand Personas ===

@app.get("/personas", tags=["Brand Personas"])
async def list_personas():
    """Lista todas as personas de marca disponíveis"""
    return {"personas": get_all_personas()}


@app.get("/personas/{persona_id}", tags=["Brand Personas"])
async def get_persona_by_id(persona_id: str):
    """Retorna uma persona específica"""
    persona = get_persona(persona_id)
    if not persona:
        raise HTTPException(status_code=404, detail="Persona não encontrada")
    return persona


@app.get("/personas/{persona_id}/guidelines", tags=["Brand Personas"])
async def get_persona_guidelines(persona_id: str):
    """Retorna diretrizes completas de tom de voz para uma persona"""
    guidelines = get_tone_guidelines(persona_id)
    if not guidelines:
        raise HTTPException(status_code=404, detail="Persona não encontrada")
    return guidelines


# === Folders ===

@app.post("/folders", tags=["Folders"])
async def create_folder(name: str, description: str = "", brand_persona_id: Optional[str] = None):
    """Cria uma nova pasta para organizar briefings relacionados"""
    folder_id = storage.create_folder(
        name=name,
        description=description,
        brand_persona_id=brand_persona_id
    )
    
    folder = storage.get_folder(folder_id)
    return {"folder_id": folder_id, "folder": folder}


@app.get("/folders", tags=["Folders"])
async def list_folders():
    """Lista todas as pastas"""
    return {"folders": storage.list_folders()}


@app.get("/folders/{folder_id}", tags=["Folders"])
async def get_folder_by_id(folder_id: str):
    """Retorna uma pasta específica"""
    folder = storage.get_folder(folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Pasta não encontrada")
    return folder


@app.get("/folders/{folder_id}/context", tags=["Folders"])
async def get_folder_context(folder_id: str):
    """Retorna o contexto de uma pasta para geração de briefings similares"""
    context = storage.get_folder_context(folder_id)
    if not context:
        raise HTTPException(status_code=404, detail="Pasta não encontrada")
    return context


@app.get("/folders/{folder_id}/briefings", tags=["Folders"])
async def list_folder_briefings(folder_id: str):
    """Lista todos os briefings de uma pasta"""
    folder = storage.get_folder(folder_id)
    if not folder:
        raise HTTPException(status_code=404, detail="Pasta não encontrada")
    
    briefings = storage.get_briefings_by_folder(folder_id)
    return {"briefings": [storage.export_briefing_to_dict(b.id) for b in briefings]}


@app.delete("/folders/{folder_id}", tags=["Folders"])
async def delete_folder(folder_id: str):
    """Deleta uma pasta (não deleta os briefings)"""
    success = storage.delete_folder(folder_id)
    if not success:
        raise HTTPException(status_code=404, detail="Pasta não encontrada")
    return {"message": "Pasta deletada com sucesso"}


# === Briefings ===

@app.post("/briefings/generate", tags=["Briefings"])
async def generate_briefing(request: GenerationRequest):
    """
    Gera um briefing baseado no input do usuário.
    
    O sistema:
    1. Detecta complexidade (simples, campanha, estratégico)
    2. Extrai informações (datas, deliverables, objetivos)
    3. Sugere template adequado
    4. Gera especificações técnicas automáticas
    5. Aplica tom de voz da marca selecionada
    6. Cria checklist de validação
    7. Identifica informações faltantes e gera perguntas
    """
    try:
        # Obtém contexto da pasta se especificado
        folder_context = None
        if request.user_input.folder_id:
            folder_context = storage.get_folder_context(request.user_input.folder_id)
        
        # Gera o briefing usando a AI Engine
        response = ai_engine.generate_briefing(
            user_input=request.user_input,
            folder_context=folder_context
        )
        
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar briefing: {str(e)}")


@app.post("/briefings/save", tags=["Briefings"])
async def save_briefing(briefing_data: Dict[str, Any]):
    """
    Salva um briefing gerado.
    
    Opções:
    - Salvar em uma pasta existente
    - Criar nova pasta
    - Manter como rascunho avulso
    """
    try:
        # Converte dicionário para modelo Briefing
        briefing = Briefing(**briefing_data)
        
        # Determina folder_id
        folder_id = briefing_data.get("folder_id")
        
        # Salva o briefing
        briefing_id = storage.save_briefing(briefing, folder_id)
        
        return {
            "briefing_id": briefing_id,
            "message": "Briefing salvo com sucesso",
            "folder_id": folder_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao salvar briefing: {str(e)}")


@app.post("/briefings/discard", tags=["Briefings"])
async def discard_briefing(briefing_id: str):
    """Descarta um briefing (rascunho não salvo)"""
    # Briefings não salvos não precisam de ação
    return {"message": "Briefing descartado"}


@app.get("/briefings", tags=["Briefings"])
async def list_briefings(limit: int = 50):
    """Lista todos os briefings salvos"""
    briefings = storage.list_briefings(limit)
    return {
        "briefings": [storage.export_briefing_to_dict(b.id) for b in briefings],
        "total": len(briefings)
    }


@app.get("/briefings/{briefing_id}", tags=["Briefings"])
async def get_briefing_by_id(briefing_id: str):
    """Retorna um briefing específico"""
    briefing_dict = storage.export_briefing_to_dict(briefing_id)
    if not briefing_dict:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    return briefing_dict


@app.put("/briefings/{briefing_id}", tags=["Briefings"])
async def update_briefing(briefing_id: str, briefing_data: Dict[str, Any]):
    """Atualiza um briefing existente"""
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Atualiza campos
    updated_briefing = Briefing(
        **{**briefing.model_dump(), **briefing_data}
    )
    updated_briefing.id = briefing_id
    
    success = storage.update_briefing(updated_briefing)
    if not success:
        raise HTTPException(status_code=500, detail="Erro ao atualizar briefing")
    
    return {"message": "Briefing atualizado com sucesso"}


@app.post("/briefings/{briefing_id}/refine", tags=["Briefings"])
async def refine_briefing(briefing_id: str, feedback: str):
    """
    Refina um briefing baseado em feedback.
    
    Exemplos de feedback:
    - "Deixe o tom mais urgente"
    - "Adicione um item para banner impresso"
    - "Mude para o tom corporativo B2B"
    """
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Usa AI Engine para refinar
    refined_briefing = ai_engine.refine_briefing(briefing, feedback)
    
    # Salva versão atualizada
    storage.update_briefing(refined_briefing)
    
    return {
        "message": "Briefing refinado com sucesso",
        "briefing": storage.export_briefing_to_dict(refined_briefing.id)
    }


@app.delete("/briefings/{briefing_id}", tags=["Briefings"])
async def delete_briefing(briefing_id: str):
    """Deleta um briefing"""
    success = storage.delete_briefing(briefing_id)
    if not success:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    return {"message": "Briefing deletado com sucesso"}


# === Export ===

@app.get("/briefings/{briefing_id}/export/json", tags=["Export"])
async def export_briefing_json(briefing_id: str):
    """Exporta briefing em formato JSON"""
    data = storage.export_briefing_to_json(briefing_id)
    if not data:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    return data


@app.get("/briefings/{briefing_id}/export/pdf", tags=["Export"])
async def export_briefing_pdf(briefing_id: str):
    """
    Exporta briefing em formato PDF.
    Em produção, geraria um PDF formatado.
    """
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Em produção, usaria uma biblioteca como fpdf ou reportlab
    # Aqui retornamos um JSON indicando que o PDF seria gerado
    return {
        "message": "PDF seria gerado aqui",
        "briefing_id": briefing_id,
        "title": briefing.title
    }


@app.get("/briefings/{briefing_id}/export/docx", tags=["Export"])
async def export_briefing_docx(briefing_id: str):
    """
    Exporta briefing em formato DOCX (Word).
    Em produção, geraria um documento Word formatado.
    """
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Em produção, usaria python-docx
    return {
        "message": "DOCX seria gerado aqui",
        "briefing_id": briefing_id,
        "title": briefing.title
    }


# === Aprovação ===

@app.post("/briefings/{briefing_id}/request-approval", tags=["Aprovação"])
async def request_approval(briefing_id: str, approver_id: str, comments: Optional[str] = None):
    """Solicita aprovação de um briefing"""
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Atualiza status
    briefing.status = "pending_approval"
    storage.update_briefing(briefing)
    
    # Em produção, enviaria notificação para o approver
    return {
        "message": "Solicitação de aprovação enviada",
        "briefing_id": briefing_id,
        "approver_id": approver_id,
        "status": "pending_approval"
    }


@app.post("/briefings/{briefing_id}/approve", tags=["Aprovação"])
async def approve_briefing(briefing_id: str, approved_by: str, comments: Optional[str] = None):
    """Aprova ou rejeita um briefing"""
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Atualiza status
    briefing.status = "approved"
    briefing.feedback = comments
    storage.update_briefing(briefing)
    
    return {
        "message": "Briefing aprovado com sucesso",
        "briefing_id": briefing_id,
        "approved_by": approved_by,
        "status": "approved"
    }


# === Integrações (Simuladas) ===

@app.post("/integrations/trello/create-card", tags=["Integrações"])
async def create_trello_card(briefing_id: str, board_id: str, list_id: str):
    """Cria um card no Trello baseado no briefing"""
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Em produção, integraria com API do Trello
    return {
        "message": "Card criado no Trello (simulação)",
        "briefing_id": briefing_id,
        "board_id": board_id,
        "list_id": list_id,
        "card_title": briefing.title
    }


@app.post("/integrations/asana/create-task", tags=["Integrações"])
async def create_asana_task(briefing_id: str, project_id: str):
    """Cria uma task no Asana baseada no briefing"""
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Em produção, integraria com API do Asana
    return {
        "message": "Task criada no Asana (simulação)",
        "briefing_id": briefing_id,
        "project_id": project_id,
        "task_name": briefing.title
    }


@app.post("/integrations/jira/create-issue", tags=["Integrações"])
async def create_jira_issue(briefing_id: str, project_key: str, issue_type: str = "Task"):
    """Cria uma issue no Jira baseada no briefing"""
    briefing = storage.get_briefing(briefing_id)
    if not briefing:
        raise HTTPException(status_code=404, detail="Briefing não encontrado")
    
    # Em produção, integraria com API do Jira
    return {
        "message": "Issue criada no Jira (simulação)",
        "briefing_id": briefing_id,
        "project_key": project_key,
        "issue_type": issue_type,
        "summary": briefing.title
    }


# === Execução ===

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
