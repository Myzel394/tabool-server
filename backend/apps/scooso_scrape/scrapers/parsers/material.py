import re
from datetime import datetime
from typing import *

from .base import BaseParser

__all__ = [
    "PureMaterialParser", "PureMaterialParserDataType"
]

from ...utils import get_safe_filename


class MaterialType(TypedDict):
    id: int
    filename: str
    owner: Optional[int]
    created_at: Optional[datetime]
    edited_at: Optional[datetime]


class PureMaterialParserDataType(TypedDict):
    materials: List[MaterialType]
    id: int


class PureMaterialParser(BaseParser):
    material_filename_regex = re.compile(r"[0-9]+_(?=.)")
    
    @classmethod
    def constrain_filename(cls, name: str) -> str:
        return cls.material_filename_regex.sub("", name)
    
    @property
    def data(self) -> PureMaterialParserDataType:
        items = self.json["tables"]["items"]
        data = []
        
        for item in items:
            data.append({
                "id": item["id"],
                "filename": self.constrain_filename(get_safe_filename(item["name"])),
                "owner": item.get("owner"),
                "created_at": item.get("created"),
                "edited_at": item.get("edited"),
            })
        
        return {
            "materials": data,
            "id": self.json["item"]["id"]
        }
    
    @property
    def is_valid(self) -> bool:
        try:
            return len(self.json["tables"].get("items", [])) > 0
        except:
            return False
