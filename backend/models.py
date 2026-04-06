"""
Modelos de dados para o Briefa - Sistema de Geração de Briefings com IA
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ComplexityLevel(str, Enum):
    SIMPLE = "simple"  # Tarefa Única
    CAMPAIGN = "campaign"  # Campanha Multi-peça
    STRATEGIC = "strategic"  # Estratégico


class BrandTone(str, Enum):
    GLPV_HUMANIZED = "glpv_humanized"  # Humanizado, Acolhedor, Esperançoso
    CORPORATE_B2B = "corporate_b2b"  # Corporativo B2B
    GEN_Z = "gen_z"  # Tom jovem Gen-Z
    EMOTIONAL = "emotional"  # Emocionante
    URGENT = "urgent"  # Urgente


class InputType(str, Enum):
    TEXT = "text"
    AUDIO = "audio"
    IMAGE_OCR = "image_ocr"
    FILE = "file"


class BrandPersona(BaseModel):
    """Perfil de Marca (Brand Persona)"""
    id: str
    name: str
    tone: str
    forbidden_words: List[str] = []
    keywords: List[str] = []
    visual_rules: List[str] = []
    description: str = ""


class BriefingItem(BaseModel):
    """Item individual do briefing"""
    title: str
    description: str
    specifications: Optional[str] = None
    deadline: Optional[str] = None
    responsible: Optional[str] = None
    status: str = "pending"


class ValidationCheck(BaseModel):
    """Item de validação do briefing"""
    item: str
    included: bool
    notes: Optional[str] = None


class Briefing(BaseModel):
    """Estrutura principal do Briefing"""
    id: Optional[str] = None
    folder_id: Optional[str] = None
    title: str
    description: str
    complexity: ComplexityLevel = ComplexityLevel.SIMPLE
    brand_tone: BrandTone = BrandTone.GLPV_HUMANIZED
    brand_persona_id: Optional[str] = None
    
    # Informações do projeto
    objective: str = ""
    target_audience: str = ""
    deliverables: List[BriefingItem] = []
    deadlines: Dict[str, str] = {}
    responsibilities: Dict[str, str] = {}
    
    # Especificações técnicas
    technical_specs: Dict[str, Any] = {}
    references: List[str] = []
    
    # Validação
    validation_checks: List[ValidationCheck] = []
    missing_info: List[str] = []
    
    # Metadados
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    version: int = 1
    status: str = "draft"  # draft, pending_approval, approved, rejected
    
    # Histórico
    versions: List[Dict[str, Any]] = []
    feedback: Optional[str] = None


class Folder(BaseModel):
    """Pasta para organizar briefings relacionados"""
    id: str
    name: str
    description: str = ""
    brand_persona_id: Optional[str] = None
    briefings: List[str] = []  # IDs dos briefings
    created_at: datetime = Field(default_factory=datetime.now)
    context_data: Dict[str, Any] = {}  # Dados para contexto entre briefings similares


class UserInput(BaseModel):
    """Entrada do usuário para geração de briefing"""
    text: str = ""
    input_type: InputType = InputType.TEXT
    audio_url: Optional[str] = None
    image_url: Optional[str] = None
    file_url: Optional[str] = None
    folder_id: Optional[str] = None
    brand_tone: Optional[BrandTone] = None
    brand_persona_id: Optional[str] = None


class GenerationRequest(BaseModel):
    """Requisição para geração de briefing"""
    user_input: UserInput
    template_id: Optional[str] = None
    regenerate: bool = False
    previous_briefing_id: Optional[str] = None


class GenerationResponse(BaseModel):
    """Resposta da geração de briefing"""
    briefing: Briefing
    suggested_template: str
    complexity_detected: ComplexityLevel
    questions_for_user: List[str] = []
    confidence_score: float = 0.0


class Template(BaseModel):
    """Template de briefing"""
    id: str
    name: str
    description: str
    complexity: ComplexityLevel
    sections: List[str]
    default_specs: Dict[str, Any] = {}


class ApprovalRequest(BaseModel):
    """Solicitação de aprovação"""
    briefing_id: str
    approver_id: str
    comments: Optional[str] = None


class ApprovalResponse(BaseModel):
    """Resposta de aprovação"""
    approved: bool
    comments: Optional[str] = None
    approved_at: datetime = Field(default_factory=datetime.now)
    approved_by: str
