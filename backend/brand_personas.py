"""
Brand Personas - Perfis de marca pré-configurados com tom de voz e diretrizes
"""
from typing import Dict, List, Any


BRAND_PERSONAS = {
    "glpv_30anos": {
        "id": "glpv_30anos",
        "name": "GLPV - 30 Anos",
        "description": "Perfil da marca GLPV para celebração de 30 anos",
        "tone": "Humanizado, Acolhedor, Esperançoso",
        "tone_attributes": [
            "humanized",
            "warm",
            "hopeful",
            "emotional",
            "inclusive"
        ],
        "forbidden_words": [
            "compre agora",
            "imperdível",
            "sensacional",
            "técnico excessivo",
            "frio",
            "sensacionalista negativo",
            "urgente demais",
            "agressivo"
        ],
        "keywords": [
            "cuidado",
            "vida",
            "juntos",
            "transformação",
            "esperança",
            "acolhimento",
            "história",
            "legado",
            "futuro",
            "comunidade",
            "amor",
            "dedicação"
        ],
        "visual_rules": [
            "Fotos reais > Banco de imagem",
            "Cores institucionais + Dourado (aniversários)",
            "Evitar imagens muito produzidas ou artificiais",
            "Priorizar diversidade e representatividade",
            "Usar luz natural e tons quandos"
        ],
        "voice_examples": {
            "instead_of": "compre agora",
            "use": "faça parte dessa história de esperança"
        },
        "brand_values": [
            "Cuidado humano",
            "Transformação de vidas",
            "Comunidade e pertencimento",
            "Esperança no futuro"
        ]
    },
    "corporate_b2b": {
        "id": "corporate_b2b",
        "name": "Corporativo B2B",
        "description": "Tom corporativo profissional para negócios B2B",
        "tone": "Profissional, Confiável, Autoritário",
        "tone_attributes": [
            "professional",
            "trustworthy",
            "authoritative",
            "clear",
            "direct"
        ],
        "forbidden_words": [
            "gírias",
            "informal demais",
            "emocional excessivo",
            "subjetivo",
            "vago"
        ],
        "keywords": [
            "solução",
            "resultados",
            "eficiência",
            "parceria",
            "inovação",
            "expertise",
            "confiança",
            "performance",
            "ROI",
            "estratégia"
        ],
        "visual_rules": [
            "Imagens limpas e profissionais",
            "Paleta de cores sóbria",
            "Tipografia clara e legível",
            "Gráficos e dados visuais",
            "Ambientes corporativos"
        ],
        "voice_examples": {
            "instead_of": "somos demais!",
            "use": "oferecemos soluções comprovadas"
        },
        "brand_values": [
            "Excelência técnica",
            "Resultados mensuráveis",
            "Parceria de longo prazo",
            "Inovação com propósito"
        ]
    },
    "gen_z_brand": {
        "id": "gen_z_brand",
        "name": "Marca Gen-Z",
        "description": "Tom jovem, autêntico e conectado com a geração Z",
        "tone": "Jovem, Autêntico, Descontraído",
        "tone_attributes": [
            "authentic",
            "casual",
            "fun",
            "relatable",
            "bold"
        ],
        "forbidden_words": [
            "formal demais",
            "corporativês",
            "rígido",
            "distante",
            "fingido"
        ],
        "keywords": [
            "real",
            "autêntico",
            "conectado",
            "diversidade",
            "propósito",
            "mudança",
            "voz",
            "comunidade",
            "experiência",
            "momento"
        ],
        "visual_rules": [
            "Estética UGC (User Generated Content)",
            "Cores vibrantes e contrastantes",
            "Tipografia moderna e ousada",
            "GIFs e elementos dinâmicos",
            "Diversidade real"
        ],
        "voice_examples": {
            "instead_of": "adquira nosso produto",
            "use": "vem fazer parte do rolê"
        },
        "brand_values": [
            "Autenticidade acima de tudo",
            "Diversidade e inclusão",
            "Propósito social",
            "Transparência"
        ]
    },
    "luxury_premium": {
        "id": "luxury_premium",
        "name": "Luxo Premium",
        "description": "Tom sofisticado para marcas de luxo e premium",
        "tone": "Sofisticado, Exclusivo, Elegante",
        "tone_attributes": [
            "sophisticated",
            "exclusive",
            "elegant",
            "refined",
            "timeless"
        ],
        "forbidden_words": [
            "barato",
            "promoção",
            "desconto",
            "popular",
            "comum",
            "acessível"
        ],
        "keywords": [
            "exclusivo",
            "singular",
            "atemporal",
            "artesanal",
            "precioso",
            "refinado",
            "elegante",
            "distinto",
            "experiência",
            "legado"
        ],
        "visual_rules": [
            "Minimalismo sofisticado",
            "Espaço em branco generoso",
            "Tipografia serifada elegante",
            "Fotografia artística",
            "Acabamentos premium"
        ],
        "voice_examples": {
            "instead_of": "aproveite agora",
            "use": "descubra uma experiência singular"
        },
        "brand_values": [
            "Excelência artesanal",
            "Exclusividade",
            "Atemporalidade",
            "Experiência memorável"
        ]
    }
}


def get_persona(persona_id: str) -> Dict[str, Any]:
    """Retorna uma persona específica pelo ID"""
    return BRAND_PERSONAS.get(persona_id, BRAND_PERSONAS["glpv_30anos"])


def get_all_personas() -> List[Dict[str, Any]]:
    """Retorna todas as personas disponíveis"""
    return list(BRAND_PERSONAS.values())


def apply_tone_to_text(text: str, persona_id: str) -> str:
    """
    Aplica o tom de voz de uma persona a um texto.
    Em produção, isso seria feito via LLM com as diretrizes da persona.
    """
    persona = get_persona(persona_id)
    
    # Simulação simples - em produção usaria IA generativa
    forbidden = persona.get("forbidden_words", [])
    keywords = persona.get("keywords", [])
    
    result = text
    for word in forbidden:
        if word.lower() in result.lower():
            # Em produção, substituiria por sugestão da IA
            result = result.replace(word, f"[{word} - considerar alternativa]")
    
    return result


def get_tone_guidelines(persona_id: str) -> Dict[str, Any]:
    """Retorna diretrizes completas de tom de voz para uma persona"""
    persona = get_persona(persona_id)
    return {
        "tone": persona["tone"],
        "attributes": persona["tone_attributes"],
        "forbidden_words": persona["forbidden_words"],
        "recommended_keywords": persona["keywords"],
        "visual_guidelines": persona["visual_rules"],
        "voice_examples": persona["voice_examples"],
        "values": persona["brand_values"]
    }
