"""
Storage - Sistema de armazenamento em memória para briefings e pastas
Em produção, substituir por banco de dados real (PostgreSQL, MongoDB, etc.)
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

from models import Briefing, Folder, BrandPersona


class Storage:
    """
    Sistema de armazenamento simples usando arquivos JSON.
    Simula a estrutura de pastas e briefings do sistema.
    """
    
    def __init__(self, base_path: str = "/workspace/data"):
        self.base_path = Path(base_path)
        self.briefings_path = self.base_path / "briefings"
        self.folders_path = self.base_path / "folders"
        self.personas_path = self.base_path / "personas"
        
        # Cria diretórios
        self.briefings_path.mkdir(parents=True, exist_ok=True)
        self.folders_path.mkdir(parents=True, exist_ok=True)
        self.personas_path.mkdir(parents=True, exist_ok=True)
        
        # Cache em memória
        self._briefings_cache: Dict[str, Briefing] = {}
        self._folders_cache: Dict[str, Folder] = {}
        self._personas_cache: Dict[str, BrandPersona] = {}
        
        # Carrega dados existentes
        self._load_all()
    
    def _load_all(self):
        """Carrega todos os dados do disco"""
        # Carrega briefings
        if self.briefings_path.exists():
            for file in self.briefings_path.glob("*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        briefing = Briefing(**data)
                        self._briefings_cache[briefing.id or file.stem] = briefing
                except Exception as e:
                    print(f"Erro ao carregar briefing {file}: {e}")
        
        # Carrega folders
        if self.folders_path.exists():
            for file in self.folders_path.glob("*.json"):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        folder = Folder(**data)
                        self._folders_cache[folder.id] = folder
                except Exception as e:
                    print(f"Erro ao carregar folder {file}: {e}")
    
    def _generate_id(self, prefix: str) -> str:
        """Gera um ID único"""
        import uuid
        return f"{prefix}_{uuid.uuid4().hex[:8]}"
    
    # === Briefings ===
    
    def save_briefing(self, briefing: Briefing, folder_id: Optional[str] = None) -> str:
        """Salva um briefing"""
        if not briefing.id:
            briefing.id = self._generate_id("brf")
        
        briefing.updated_at = datetime.now()
        
        # Salva no cache
        self._briefings_cache[briefing.id] = briefing
        
        # Salva em arquivo
        file_path = self.briefings_path / f"{briefing.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(briefing.model_dump(mode='json'), f, indent=2, ensure_ascii=False)
        
        # Associa à pasta se especificado
        if folder_id:
            self.add_briefing_to_folder(folder_id, briefing.id)
            briefing.folder_id = folder_id
        
        return briefing.id
    
    def get_briefing(self, briefing_id: str) -> Optional[Briefing]:
        """Recupera um briefing pelo ID"""
        return self._briefings_cache.get(briefing_id)
    
    def get_briefings_by_folder(self, folder_id: str) -> List[Briefing]:
        """Recupera todos os briefings de uma pasta"""
        folder = self.get_folder(folder_id)
        if not folder:
            return []
        
        return [
            self._briefings_cache[b_id] 
            for b_id in folder.briefings 
            if b_id in self._briefings_cache
        ]
    
    def update_briefing(self, briefing: Briefing) -> bool:
        """Atualiza um briefing existente"""
        if not briefing.id or briefing.id not in self._briefings_cache:
            return False
        
        briefing.updated_at = datetime.now()
        self._briefings_cache[briefing.id] = briefing
        
        file_path = self.briefings_path / f"{briefing.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(briefing.model_dump(mode='json'), f, indent=2, ensure_ascii=False)
        
        return True
    
    def delete_briefing(self, briefing_id: str) -> bool:
        """Deleta um briefing"""
        if briefing_id not in self._briefings_cache:
            return False
        
        briefing = self._briefings_cache[briefing_id]
        
        # Remove da pasta se estiver associado
        if briefing.folder_id:
            self.remove_briefing_from_folder(briefing.folder_id, briefing_id)
        
        # Remove do cache e arquivo
        del self._briefings_cache[briefing_id]
        file_path = self.briefings_path / f"{briefing_id}.json"
        if file_path.exists():
            file_path.unlink()
        
        return True
    
    def list_briefings(self, limit: int = 50) -> List[Briefing]:
        """Lista todos os briefings"""
        return list(self._briefings_cache.values())[:limit]
    
    # === Folders ===
    
    def create_folder(self, name: str, description: str = "", brand_persona_id: Optional[str] = None) -> str:
        """Cria uma nova pasta"""
        folder = Folder(
            id=self._generate_id("fld"),
            name=name,
            description=description,
            brand_persona_id=brand_persona_id,
            briefings=[]
        )
        
        self._folders_cache[folder.id] = folder
        self._save_folder(folder)
        
        return folder.id
    
    def get_folder(self, folder_id: str) -> Optional[Folder]:
        """Recupera uma pasta pelo ID"""
        return self._folders_cache.get(folder_id)
    
    def get_folder_context(self, folder_id: str) -> Dict[str, Any]:
        """Retorna o contexto de uma pasta para geração de briefings similares"""
        folder = self.get_folder(folder_id)
        if not folder:
            return {}
        
        briefings = self.get_briefings_by_folder(folder_id)
        
        # Extrai padrões dos briefings existentes
        context = {
            "folder_id": folder_id,
            "folder_name": folder.name,
            "brand_persona_id": folder.brand_persona_id,
            "briefing_count": len(briefings),
            "common_deliverables": [],
            "common_tones": [],
            "recent_objectives": []
        }
        
        # Analisa briefings para encontrar padrões
        all_deliverables = []
        all_tones = []
        all_objectives = []
        
        for briefing in briefings[-5:]:  # Últimos 5 briefings
            for item in briefing.deliverables:
                all_deliverables.append(item.title.lower())
            if briefing.objective:
                all_objectives.append(briefing.objective)
            all_tones.append(str(briefing.brand_tone))
        
        # Encontra os mais comuns
        if all_deliverables:
            from collections import Counter
            common = Counter(all_deliverables).most_common(3)
            context["common_deliverables"] = [item[0] for item in common]
        
        context["recent_objectives"] = all_objectives[-3:]
        context["common_tones"] = list(set(all_tones))
        
        # Atualiza o cache da pasta com o contexto
        folder.context_data = context
        self._save_folder(folder)
        
        return context
    
    def add_briefing_to_folder(self, folder_id: str, briefing_id: str) -> bool:
        """Adiciona um briefing a uma pasta"""
        folder = self.get_folder(folder_id)
        if not folder:
            return False
        
        if briefing_id not in folder.briefings:
            folder.briefings.append(briefing_id)
            self._save_folder(folder)
        
        # Atualiza o briefing com o folder_id
        briefing = self.get_briefing(briefing_id)
        if briefing:
            briefing.folder_id = folder_id
            self.update_briefing(briefing)
        
        return True
    
    def remove_briefing_from_folder(self, folder_id: str, briefing_id: str) -> bool:
        """Remove um briefing de uma pasta"""
        folder = self.get_folder(folder_id)
        if not folder:
            return False
        
        if briefing_id in folder.briefings:
            folder.briefings.remove(briefing_id)
            self._save_folder(folder)
        
        return True
    
    def list_folders(self) -> List[Folder]:
        """Lista todas as pastas"""
        return list(self._folders_cache.values())
    
    def delete_folder(self, folder_id: str) -> bool:
        """Deleta uma pasta (não deleta os briefings)"""
        if folder_id not in self._folders_cache:
            return False
        
        folder = self._folders_cache[folder_id]
        
        # Desassocia briefings
        for briefing_id in folder.briefings:
            briefing = self.get_briefing(briefing_id)
            if briefing:
                briefing.folder_id = None
                self.update_briefing(briefing)
        
        del self._folders_cache[folder_id]
        file_path = self.folders_path / f"{folder_id}.json"
        if file_path.exists():
            file_path.unlink()
        
        return True
    
    def _save_folder(self, folder: Folder):
        """Salva uma pasta em arquivo"""
        file_path = self.folders_path / f"{folder.id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(folder.model_dump(mode='json'), f, indent=2, ensure_ascii=False)
    
    # === Export ===
    
    def export_briefing_to_json(self, briefing_id: str) -> Optional[Dict[str, Any]]:
        """Exporta um briefing como dicionário JSON"""
        briefing = self.get_briefing(briefing_id)
        if not briefing:
            return None
        return briefing.model_dump(mode='json')
    
    def export_briefing_to_dict(self, briefing_id: str) -> Optional[Dict[str, Any]]:
        """Exporta um briefing formatado para visualização"""
        briefing = self.get_briefing(briefing_id)
        if not briefing:
            return None
        
        return {
            "id": briefing.id,
            "title": briefing.title,
            "description": briefing.description,
            "complexity": briefing.complexity.value,
            "brand_tone": briefing.brand_tone.value,
            "objective": briefing.objective,
            "target_audience": briefing.target_audience,
            "deliverables": [
                {
                    "title": item.title,
                    "description": item.description,
                    "specifications": item.specifications,
                    "deadline": item.deadline,
                    "status": item.status
                }
                for item in briefing.deliverables
            ],
            "deadlines": briefing.deadlines,
            "technical_specs": briefing.technical_specs,
            "validation_checks": [
                {"item": check.item, "included": check.included, "notes": check.notes}
                for check in briefing.validation_checks
            ],
            "missing_info": briefing.missing_info,
            "created_at": briefing.created_at.isoformat(),
            "updated_at": briefing.updated_at.isoformat(),
            "version": briefing.version,
            "status": briefing.status
        }


# Singleton instance
storage = Storage()
