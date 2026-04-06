"""
Templates de Briefing - Modelos pré-configurados para diferentes tipos de projeto
"""
from typing import Dict, Any, List


TEMPLATES = {
    "post_single": {
        "id": "post_single",
        "name": "Post+Story (Modelo 1)",
        "description": "Template para post único em redes sociais com story complementar",
        "complexity": "simple",
        "sections": [
            "Objetivo do Post",
            "Público-Alvo",
            "Mensagem Principal",
            "Tom de Voz",
            "Formatos e Especificações",
            "Copy Sugerida",
            "Referências Visuais",
            "Prazo de Entrega"
        ],
        "default_specs": {
            "instagram_post": {
                "size": "1080x1080px",
                "format": "PNG/JPG",
                "safe_zone": "Margem de 50px nas bordas"
            },
            "instagram_story": {
                "size": "1080x1920px",
                "format": "PNG/JPG/MP4",
                "safe_zone": "350px na base (evitar UI elements)"
            }
        }
    },
    "campaign_complete": {
        "id": "campaign_complete",
        "name": "Campanha Completa (Modelo 2)",
        "description": "Template para campanhas multi-peça com múltiplos formatos e canais",
        "complexity": "campaign",
        "sections": [
            "Visão Geral da Campanha",
            "Objetivos e KPIs",
            "Público-Alvo e Personas",
            "Conceito Criativo",
            "Tom de Voz da Marca",
            "Peças Necessárias",
            "Cronograma Reverso",
            "Responsabilidades",
            "Especificações Técnicas por Peça",
            "Orçamento Estimado",
            "Referências",
            "Checklist de Validação"
        ],
        "default_specs": {
            "social_media": {
                "posts_feed": "1080x1080px ou 1080x1350px",
                "stories": "1080x1920px",
                "reels": "1080x1920px, até 90 segundos",
                "thumbnails": "1280x720px"
            },
            "paid_media": {
                "facebook_ads": "1200x628px (feed), 1080x1920px (stories)",
                "google_display": "300x250, 728x90, 160x600",
                "linkedin_ads": "1200x627px"
            },
            "print": {
                "flyer_a5": "148x210mm + 3mm bleed",
                "banner": "Dimensionar conforme necessidade",
                "business_card": "90x50mm + 3mm bleed"
            }
        }
    },
    "corporate_event": {
        "id": "corporate_event",
        "name": "Evento Corporativo (Modelo 3)",
        "description": "Template para eventos corporativos, lançamentos e celebrações",
        "complexity": "campaign",
        "sections": [
            "Dados do Evento",
            "Objetivo do Evento",
            "Público Esperado",
            "Tema e Conceito",
            "Tom de Voz",
            "Peças de Comunicação",
            "Identidade Visual",
            "Cronograma de Produção",
            "Equipe e Responsáveis",
            "Checklist de Itens",
            "Especificações Técnicas"
        ],
        "default_specs": {
            "invitation": {
                "digital": "1920x1080px ou A4 digital",
                "print": "A5 ou 15x15cm + acabamento especial"
            },
            "presentation": {
                "slides": "1920x1080px (16:9)",
                "template": "Padrão institucional da marca"
            },
            "signage": {
                "backdrop": "Dimensionar conforme espaço",
                "banners": "Variável - consultar local",
                "credenciamento": "10x15cm ou 8x12cm"
            }
        }
    },
    "brand_refresh": {
        "id": "brand_refresh",
        "name": "Refresh de Marca",
        "description": "Template para projetos de atualização de identidade visual",
        "complexity": "strategic",
        "sections": [
            "Contexto do Projeto",
            "Diagnóstico Atual",
            "Objetivos do Refresh",
            "Público-Alvo Atual vs. Desejado",
            "Valores e Posicionamento",
            "Diretrizes de Tom de Voz",
            "Elementos a Serem Atualizados",
            "Referências e Benchmarks",
            "Restrições e Requisitos",
            "Cronograma Macro",
            "Stakeholders e Aprovações"
        ],
        "default_specs": {
            "deliverables": [
                "Logotipo (versões primária, secundária, monocromática)",
                "Paleta de cores",
                "Tipografia",
                "Sistema de imagens",
                "Aplicações (papelaria, digital, signage)",
                "Brand Guidelines"
            ]
        }
    },
    "video_production": {
        "id": "video_production",
        "name": "Produção de Vídeo",
        "description": "Template para produção de vídeos institucionais, comerciais ou conteúdo",
        "complexity": "campaign",
        "sections": [
            "Objetivo do Vídeo",
            "Público-Alvo",
            "Mensagem Central",
            "Tom e Estilo",
            "Duração Estimada",
            "Formatos de Entrega",
            "Roteiro/Briefing Criativo",
            "Referências Visuais",
            "Locução/Trilha Sonora",
            "Prazos de Produção",
            "Equipe Necessária"
        ],
        "default_specs": {
            "youtube": {
                "resolution": "1920x1080 (Full HD) ou 3840x2160 (4K)",
                "aspect_ratio": "16:9",
                "max_length": "15 minutos (padrão)"
            },
            "instagram_reels": {
                "resolution": "1080x1920",
                "aspect_ratio": "9:16",
                "max_length": "90 segundos"
            },
            "linkedin": {
                "resolution": "1920x1080 ou 1080x1080",
                "max_length": "10 minutos"
            }
        }
    }
}


def get_template(template_id: str) -> Dict[str, Any]:
    """Retorna um template específico pelo ID"""
    return TEMPLATES.get(template_id, TEMPLATES["post_single"])


def get_templates_by_complexity(complexity: str) -> List[Dict[str, Any]]:
    """Retorna todos os templates de uma complexidade específica"""
    return [t for t in TEMPLATES.values() if t["complexity"] == complexity]


def get_all_templates() -> List[Dict[str, Any]]:
    """Retorna todos os templates disponíveis"""
    return list(TEMPLATES.values())
