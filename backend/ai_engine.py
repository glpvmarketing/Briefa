"""
AI Engine - Motor de Inteligência Artificial para geração e processamento de briefings
"""
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from openai import OpenAI

from models import (
    Briefing, BriefingItem, ValidationCheck, ComplexityLevel, 
    BrandTone, UserInput, GenerationResponse
)
from templates import get_template, get_all_templates
from brand_personas import get_persona, get_tone_guidelines


# Configuração da API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "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")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openrouter.ai/api/v1")

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


class AIEngine:
    """
    Motor de IA para análise, classificação e geração de briefings.
    Em produção, integraria com APIs de LLM (OpenAI, Anthropic, etc.)
    """
    
    def __init__(self):
        self.templates = get_all_templates()
        
        # Padrões para detecção de complexidade
        self.complexity_patterns = {
            "simple": [
                r"post\s*(único|simples)",
                r"story\s*(só|apenas)",
                r"arte\s*(única|avulsa)",
                r"uma?\s+(peça|imagem|arte|post)"
            ],
            "campaign": [
                r"campanha",
                r"múltipl[oa]s?\s+(peças|formatos|posts)",
                r"série\s+de",
                r"vários?\s+(posts|artes|formatos)",
                r"lançamento",
                r"evento",
                r"coleção"
            ],
            "strategic": [
                r"estratégia",
                r"posicionamento",
                r"rebrand",
                r"refresh\s+de\s+marca",
                r"identidade\s+visual",
                r"planejamento"
            ]
        }
        
        # Padrões para extração de informações
        self.date_patterns = [
            r"(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})",  # 03/06/2024 ou 03-06-2024
            r"(\d{1,2}\s+de\s+\w+)",  # 3 de junho
            r"(dia\s+\d{1,2}[/-]\d{1,2})",  # dia 03/06
            r"(hoje|amanhã|próxima?\s+\w+)"  # hoje, amanhã, próxima semana
        ]
        
        self.deliverable_keywords = {
            "posts": ["post", "posts", "feed"],
            "stories": ["story", "stories"],
            "reels": ["reel", "reels", "vídeo curto"],
            "thumbnails": ["thumb", "thumbnail", "capa"],
            "banners": ["banner", "banners"],
            "invitations": ["convite", "convites", "invitation"],
            "print": ["papel timbrado", "impresso", "gráfica"],
            "landing_page": ["landing page", "página de captura", "LP"],
            "email": ["e-mail", "email", "newsletter"]
        }
    
    def detect_complexity(self, text: str) -> ComplexityLevel:
        """Detecta o nível de complexidade do briefing baseado no input"""
        text_lower = text.lower()
        
        # Verifica padrões estratégicos primeiro (mais específicos)
        for pattern in self.complexity_patterns["strategic"]:
            if re.search(pattern, text_lower):
                return ComplexityLevel.STRATEGIC
        
        # Verifica padrões de campanha
        campaign_matches = sum(
            1 for pattern in self.complexity_patterns["campaign"]
            if re.search(pattern, text_lower)
        )
        
        if campaign_matches >= 1:
            return ComplexityLevel.CAMPAIGN
        
        # Verifica padrões simples
        simple_matches = sum(
            1 for pattern in self.complexity_patterns["simple"]
            if re.search(pattern, text_lower)
        )
        
        if simple_matches >= 1 or len(text_lower.split()) < 30:
            return ComplexityLevel.SIMPLE
        
        # Default para campanhas se houver múltiplos deliverables
        deliverables_count = sum(
            len([k for k in keywords if k in text_lower])
            for keywords in self.deliverable_keywords.values()
        )
        
        if deliverables_count >= 3:
            return ComplexityLevel.CAMPAIGN
        
        return ComplexityLevel.SIMPLE
    
    def extract_dates(self, text: str) -> List[Tuple[str, str]]:
        """Extrai datas mencionadas no texto"""
        dates = []
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                dates.append((match, "deadline"))
        return dates
    
    def extract_deliverables(self, text: str) -> List[str]:
        """Extrai deliverables mencionados no texto"""
        text_lower = text.lower()
        found = []
        
        for deliverable, keywords in self.deliverable_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found.append(deliverable)
                    break
        
        return list(set(found))
    
    def suggest_template(self, complexity: ComplexityLevel, deliverables: List[str]) -> str:
        """Sugere o template mais adequado baseado na complexidade e deliverables"""
        if complexity == ComplexityLevel.STRATEGIC:
            return "brand_refresh"
        
        if complexity == ComplexityLevel.CAMPAIGN:
            # Verifica se é evento
            if any(d in deliverables for d in ["invitations", "print", "banners"]):
                return "corporate_event"
            return "campaign_complete"
        
        # Simple
        if "reels" in deliverables or "videos" in deliverables:
            return "video_production"
        
        return "post_single"
    
    def generate_questions(self, text: str, complexity: ComplexityLevel) -> List[str]:
        """Gera perguntas para completar informações faltantes"""
        questions = []
        text_lower = text.lower()
        
        # Informações essenciais sempre necessárias
        if not any(date_pattern in text_lower for date_pattern in ["dia", "data", "prazo", "deadline", "para", "até"]):
            questions.append("Qual é a data de entrega ou lançamento?")
        
        if not any(word in text_lower for word in ["público", "audiência", "para quem", "target"]):
            questions.append("Qual é o público-alvo desta peça/campanha?")
        
        if not any(word in text_lower for word in ["objetivo", "propósito", "queremos", "precisamos"]):
            questions.append("Qual é o objetivo principal (vendas, awareness, engajamento)?")
        
        # Perguntas específicas por complexidade
        if complexity == ComplexityLevel.CAMPAIGN:
            if not any(word in text_lower for word in ["orçamento", "budget", "investimento"]):
                questions.append("Existe um orçamento estimado para esta campanha?")
            
            if not any(word in text_lower for word in ["canais", "onde", "mídia"]):
                questions.append("Quais canais de distribuição serão utilizados?")
        
        if complexity == ComplexityLevel.STRATEGIC:
            if not any(word in text_lower for word in ["concorrência", "benchmark", "referência"]):
                questions.append("Existem benchmarks ou concorrentes de referência?")
            
            if not any(word in text_lower for word in ["timeline", "cronograma", "prazos"]):
                questions.append("Qual é o timeline esperado para este projeto estratégico?")
        
        return questions[:5]  # Limita a 5 perguntas
    
    def generate_technical_specs(self, deliverables: List[str], complexity: ComplexityLevel) -> Dict[str, Any]:
        """Gera especificações técnicas automáticas baseadas nos deliverables"""
        specs = {}
        
        if "posts" in deliverables or "stories" in deliverables:
            specs["instagram"] = {
                "post_feed": {
                    "size": "1080x1080px (quadrado) ou 1080x1350px (retrato)",
                    "format": "PNG ou JPG",
                    "color_mode": "RGB",
                    "safe_zone": "Margem de 50px nas bordas para evitar cortes"
                },
                "stories": {
                    "size": "1080x1920px",
                    "format": "PNG, JPG ou MP4",
                    "safe_zone": "350px na base (evitar UI elements do Instagram)",
                    "duration": "Até 15 segundos por story (vídeo)"
                }
            }
        
        if "reels" in deliverables:
            specs["reels"] = {
                "size": "1080x1920px",
                "aspect_ratio": "9:16",
                "format": "MP4",
                "max_duration": "90 segundos",
                "fps": "30 fps recomendado",
                "safe_zones": "Evitar elementos nas bordas (UI do Reels)"
            }
        
        if "thumbnails" in deliverables:
            specs["thumbnails"] = {
                "youtube": "1280x720px (mínimo), 1920x1080px (ideal)",
                "format": "JPG ou PNG",
                "text": "Texto grande e legível em mobile"
            }
        
        if "banners" in deliverables:
            specs["banners"] = {
                "digital": "Dimensionar conforme plataforma (ex: 728x90, 300x250, 160x600)",
                "print": "Consultar gráfica para dimensões exatas + 3mm bleed",
                "resolution": "300 DPI para impressão, 72 DPI para digital"
            }
        
        if "invitations" in deliverables:
            specs["invitations"] = {
                "digital": "1920x1080px ou A4 (210x297mm) em PDF",
                "print": "A5 (148x210mm) ou 15x15cm + 3mm bleed",
                "finish": "Considerar acabamento especial para eventos premium"
            }
        
        if "print" in deliverables:
            specs["print_general"] = {
                "resolution": "300 DPI mínimo",
                "color_mode": "CMYK para impressão",
                "bleed": "3mm de sangria em todas as bordas",
                "fonts": "Converter fontes em curvas ou embedar no PDF"
            }
        
        return specs
    
    def generate_validation_checks(self, complexity: ComplexityLevel, deliverables: List[str]) -> List[ValidationCheck]:
        """Gera checklist de validação do briefing"""
        checks = []
        
        # Validações básicas (sempre presentes)
        checks.append(ValidationCheck(item="Objetivo claro definido", included=True))
        checks.append(ValidationCheck(item="Público-alvo especificado", included=True))
        checks.append(ValidationCheck(item="Data de entrega definida", included=True))
        checks.append(ValidationCheck(item="Tom de voz selecionado", included=True))
        
        # Validações por tipo de deliverable
        if "posts" in deliverables or "stories" in deliverables:
            checks.append(ValidationCheck(item="Especificações de formato incluídas", included=True))
            checks.append(ValidationCheck(item="Copy sugerida", included=False))
        
        if complexity == ComplexityLevel.CAMPAIGN:
            checks.append(ValidationCheck(item="Cronograma reverso criado", included=True))
            checks.append(ValidationCheck(item="Responsabilidades definidas", included=True))
            checks.append(ValidationCheck(item="Orçamento estimado", included=False))
        
        if complexity == ComplexityLevel.STRATEGIC:
            checks.append(ValidationCheck(item="Stakeholders identificados", included=False))
            checks.append(ValidationCheck(item="KPIs definidos", included=False))
        
        return checks
    
    def apply_brand_tone(self, content: str, persona_id: Optional[str]) -> str:
        """Aplica o tom de voz da marca ao conteúdo"""
        if not persona_id:
            return content
        
        persona = get_persona(persona_id)
        
        # Em produção, isso seria feito via LLM
        # Aqui fazemos uma simulação simples
        result = content
        
        # Adiciona keywords da persona quando apropriado
        keywords = persona.get("keywords", [])
        
        # Marca palavras proibidas para revisão
        forbidden = persona.get("forbidden_words", [])
        for word in forbidden:
            if word.lower() in result.lower():
                result = result.replace(
                    word, 
                    f"[{word} ⚠️ revisar - considerar alternativas da marca]"
                )
        
        return result
    
    def calculate_reverse_timeline(self, deadline: str, complexity: ComplexityLevel) -> Dict[str, str]:
        """Calcula cronograma reverso baseado na data final"""
        # Em produção, parsearia a data corretamente
        # Aqui usamos datas relativas simuladas
        
        try:
            deadline_date = datetime.now() + timedelta(days=14)  # Simulação
            
            if complexity == ComplexityLevel.SIMPLE:
                return {
                    "Briefing aprovado": (deadline_date - timedelta(days=10)).strftime("%d/%m"),
                    "Primeira versão": (deadline_date - timedelta(days=7)).strftime("%d/%m"),
                    "Revisões": (deadline_date - timedelta(days=4)).strftime("%d/%m"),
                    "Versão final": (deadline_date - timedelta(days=2)).strftime("%d/%m"),
                    "Entrega": deadline_date.strftime("%d/%m")
                }
            elif complexity == ComplexityLevel.CAMPAIGN:
                return {
                    "Briefing aprovado": (deadline_date - timedelta(days=20)).strftime("%d/%m"),
                    "Conceito criativo": (deadline_date - timedelta(days=15)).strftime("%d/%m"),
                    "Produção das peças": (deadline_date - timedelta(days=10)).strftime("%d/%m"),
                    "Revisões e ajustes": (deadline_date - timedelta(days=5)).strftime("%d/%m"),
                    "Aprovação final": (deadline_date - timedelta(days=2)).strftime("%d/%m"),
                    "Lançamento": deadline_date.strftime("%d/%m")
                }
            else:  # Strategic
                return {
                    "Kickoff": (deadline_date - timedelta(days=45)).strftime("%d/%m"),
                    "Pesquisa e diagnóstico": (deadline_date - timedelta(days=30)).strftime("%d/%m"),
                    "Diretrizes estratégicas": (deadline_date - timedelta(days=20)).strftime("%d/%m"),
                    "Desenvolvimento": (deadline_date - timedelta(days=10)).strftime("%d/%m"),
                    "Apresentação": (deadline_date - timedelta(days=3)).strftime("%d/%m"),
                    "Entrega final": deadline_date.strftime("%d/%m")
                }
        except Exception:
            return {"Cronograma": "A definir"}
    
    def _call_llm(self, prompt: str, system_prompt: str = "Você é um assistente especializado em criação de briefings profissionais para agências de publicidade e marketing.") -> str:
        """Chama a API de LLM para gerar conteúdo"""
        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-3.2-3b-instruct",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erro na chamada da API: {e}")
            return ""
    
    def generate_briefing(
        self, 
        user_input: UserInput, 
        folder_context: Optional[Dict[str, Any]] = None
    ) -> GenerationResponse:
        """Gera um briefing completo baseado no input do usuário usando IA real"""
        
        # 1. Detecta complexidade
        complexity = self.detect_complexity(user_input.text)
        
        # 2. Extrai informações
        dates = self.extract_dates(user_input.text)
        deliverables = self.extract_deliverables(user_input.text)
        
        # 3. Sugere template
        template_id = self.suggest_template(complexity, deliverables)
        template = get_template(template_id)
        
        # 4. Prepara contexto da persona
        persona = get_persona(user_input.brand_persona_id or "glpv_30anos")
        tone_guidelines = get_tone_guidelines(user_input.brand_persona_id or "glpv_30anos")
        
        # 5. Monta prompt para a IA
        system_prompt = f"""Você é um especialista em criação de briefings profissionais para agências de publicidade.
Sua tarefa é transformar solicitações informais em briefings estruturados e prontos para execução.

Persona da Marca:
- Nome: {persona.get('name', 'Não especificado')}
- Tom: {persona.get('tone', 'Não especificado')}
- Palavras-chave: {', '.join(persona.get('keywords', []))}
- Palavras proibidas: {', '.join(persona.get('forbidden_words', []))}

Diretrizes de Tom de Voz:
{tone_guidelines}

Sempre gere respostas em português do Brasil."""

        context_info = ""
        if folder_context and folder_context.get("previous_briefings"):
            context_info = "\n\nContexto de Projetos Anteriores nesta Pasta:\n"
            for prev in folder_context["previous_briefings"][-3:]:
                context_info += f"- {prev.get('title', 'Sem título')}: {prev.get('description', '')[:100]}...\n"

        prompt = f"""Transforme esta solicitação em um briefing profissional estruturado:

Solicitação do Usuário:
"{user_input.text}"

{context_info}

Complexidade Detectada: {complexity.value}
Deliverables Identificados: {', '.join(deliverables) if deliverables else 'Não especificado'}
Template Sugerido: {template_id}

Por favor, gere:
1. Um título claro e objetivo (máximo 80 caracteres)
2. Uma descrição detalhada aplicando o tom de voz da marca
3. Objetivo principal do projeto
4. Público-alvo sugerido (se não mencionado, inferir baseado no contexto)
5. Lista de deliverables com especificações técnicas apropriadas
6. Cronograma reverso sugerido (se houver data mencionada)
7. Checklist de validação

Responda EXATAMENTE neste formato JSON:
{{
    "title": "título aqui",
    "description": "descrição aqui",
    "objective": "objetivo aqui",
    "target_audience": "público aqui",
    "deliverables": [
        {{"title": "Post", "description": "...", "specifications": "..."}}
    ],
    "deadlines": {{"Briefing aprovado": "01/01", "Entrega": "15/01"}},
    "missing_info": ["pergunta 1", "pergunta 2"]
}}"""

        # 6. Chama a IA
        llm_response = self._call_llm(prompt, system_prompt)
        
        # 7. Parse da resposta da IA
        import json
        parsed_data = {}
        try:
            # Tenta extrair JSON da resposta
            start_idx = llm_response.find('{')
            end_idx = llm_response.rfind('}') + 1
            if start_idx >= 0 and end_idx > start_idx:
                json_str = llm_response[start_idx:end_idx]
                parsed_data = json.loads(json_str)
        except Exception as e:
            print(f"Erro ao parsear resposta da IA: {e}")
            parsed_data = {}
        
        # 8. Gera especificações técnicas
        tech_specs = self.generate_technical_specs(deliverables, complexity)
        
        # 9. Gera validações
        validation_checks = self.generate_validation_checks(complexity, deliverables)
        
        # 10. Gera perguntas para informações faltantes
        questions = parsed_data.get("missing_info", [])
        if not questions:
            questions = self.generate_questions(user_input.text, complexity)
        
        # 11. Cálculo de timeline
        deadlines = parsed_data.get("deadlines", {})
        if not deadlines and dates:
            deadlines = self.calculate_reverse_timeline(dates[0][0], complexity)
        
        # 12. Monta o briefing com dados da IA
        title = parsed_data.get("title", self._generate_title(user_input.text, complexity))
        description = parsed_data.get("description", "")
        if not description:
            description = self.apply_brand_tone(user_input.text, user_input.brand_persona_id)
        
        # Cria deliverables estruturados
        briefing_items = []
        ai_deliverables = parsed_data.get("deliverables", [])
        
        if ai_deliverables:
            for item in ai_deliverables:
                briefing_items.append(BriefingItem(
                    title=item.get("title", "Item"),
                    description=item.get("description", ""),
                    specifications=item.get("specifications", tech_specs.get(item.get("title", "").lower(), "Ver especificações")),
                    status="pending"
                ))
        else:
            # Fallback para deliverables detectados
            for deliverable in deliverables:
                specs = tech_specs.get(deliverable, {})
                specs_str = str(specs) if isinstance(specs, dict) else (specs or "Ver especificações gerais")
                briefing_items.append(BriefingItem(
                    title=deliverable.capitalize(),
                    description=f"Criar {deliverable} conforme especificações técnicas",
                    specifications=specs_str,
                    status="pending"
                ))
        
        # Se ainda não tem deliverables, cria genérico
        if not briefing_items:
            briefing_items.append(BriefingItem(
                title="Peça Principal",
                description="Criar peça conforme solicitado",
                specifications="Ver especificações técnicas",
                status="pending"
            ))
        
        # 13. Calcula confidence score
        confidence_score = self._calculate_confidence(
            user_input.text, 
            complexity, 
            len(questions)
        )
        
        # Aumenta confiança se a IA conseguiu gerar dados úteis
        if parsed_data:
            confidence_score = min(1.0, confidence_score + 0.15)
        
        # Cria o briefing
        briefing = Briefing(
            title=title,
            description=description,
            complexity=complexity,
            brand_tone=user_input.brand_tone or BrandTone.GLPV_HUMANIZED,
            brand_persona_id=user_input.brand_persona_id or "glpv_30anos",
            objective=parsed_data.get("objective", self._extract_objective(user_input.text)),
            target_audience=parsed_data.get("target_audience", ""),
            deliverables=briefing_items,
            deadlines=deadlines,
            technical_specs=tech_specs,
            validation_checks=validation_checks,
            missing_info=questions
        )
        
        return GenerationResponse(
            briefing=briefing,
            suggested_template=template_id,
            complexity_detected=complexity,
            questions_for_user=questions,
            confidence_score=confidence_score
        )
    
    def _generate_title(self, text: str, complexity: ComplexityLevel) -> str:
        """Gera título para o briefing"""
        words = text.split()[:8]
        base_title = " ".join(words).strip()
        
        if complexity == ComplexityLevel.SIMPLE:
            return f"Post: {base_title}"
        elif complexity == ComplexityLevel.CAMPAIGN:
            return f"Campanha: {base_title}"
        else:
            return f"Estratégico: {base_title}"
    
    def _generate_description(self, text: str, persona_id: str) -> str:
        """Gera descrição aplicando tom de voz"""
        # Em produção, reescreveria com IA
        return self.apply_brand_tone(text, persona_id)
    
    def _extract_objective(self, text: str) -> str:
        """Extrai objetivo do texto"""
        # Simples extração baseada em palavras-chave
        objective_patterns = [
            r"(preciso|necessito|queremos|objetivo):\s*(.+?)(?:\.|$)",
            r"para\s+(.+?)(?:\.|$)",
            r"focado\s+em\s+(.+?)(?:\.|$)"
        ]
        
        for pattern in objective_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return "Não especificado"
    
    def _calculate_confidence(self, text: str, complexity: ComplexityLevel, missing_count: int) -> float:
        """Calcula score de confiança da geração"""
        base_score = 0.9
        
        # Penaliza por informações faltantes
        penalty = missing_count * 0.1
        
        # Penaliza se texto muito curto para complexidade alta
        word_count = len(text.split())
        if complexity == ComplexityLevel.CAMPAIGN and word_count < 30:
            penalty += 0.15
        elif complexity == ComplexityLevel.STRATEGIC and word_count < 50:
            penalty += 0.2
        
        return max(0.3, min(1.0, base_score - penalty))
    
    def refine_briefing(
        self, 
        briefing: Briefing, 
        feedback: str,
        folder_context: Optional[Dict[str, Any]] = None
    ) -> Briefing:
        """Refina um briefing existente baseado em feedback"""
        # Em produção, usaria IA para entender o feedback e ajustar
        # Aqui fazemos ajustes básicos
        
        updated_briefing = briefing.copy()
        updated_briefing.updated_at = datetime.now()
        updated_briefing.version += 1
        
        # Salva versão anterior
        updated_briefing.versions.append({
            "version": briefing.version,
            "updated_at": briefing.updated_at.isoformat(),
            "changes": feedback
        })
        
        # Processa feedback
        feedback_lower = feedback.lower()
        
        if "tom" in feedback_lower and ("mais" in feedback_lower or "menos" in feedback_lower):
            updated_briefing.description = f"{briefing.description} [Tom ajustado conforme feedback: {feedback}]"
        
        if "adicionar" in feedback_lower or "incluir" in feedback_lower:
            # Tenta extrair o que deve ser adicionado
            updated_briefing.missing_info = []
        
        if "urgente" in feedback_lower:
            updated_briefing.brand_tone = BrandTone.URGENT
        
        return updated_briefing


# Singleton instance
ai_engine = AIEngine()
