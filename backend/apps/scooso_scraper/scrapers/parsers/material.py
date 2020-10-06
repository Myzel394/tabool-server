import re
from datetime import datetime
from pathlib import Path
from typing import *

from django.utils.translation import gettext_lazy as _

from .base import BaseParser
from ... import constants

__all__ = [
    "PureMaterialParser", "PureMaterialParserDataType"
]

from ...utils import get_safe_filename


class MaterialType(TypedDict):
    id: int
    filename: str
    owner_id: Optional[int]
    created_at: Optional[datetime]
    edited_at: Optional[datetime]


class PureMaterialParserDataType(TypedDict):
    materials: List[MaterialType]
    id: int


class PureMaterialParser(BaseParser):
    material_filename_regex = re.compile(r"[0-9]+_(?=.)")
    unnamed_material_filename_regex = re.compile(constants.UNNAMED_FILE_DETECT_REGEX, re.RegexFlag.I)
    
    @classmethod
    def constrain_filename(cls, name: str) -> str:
        return cls.material_filename_regex.sub("", name)
    
    @classmethod
    def get_any_filename(cls, name: str) -> str:
        if cls.unnamed_material_filename_regex.match(name):
            return str(_(constants.UNNAMED_FILE_REPLACE_NAME)) + Path(name).suffix
        return name
    
    @property
    def data(self) -> PureMaterialParserDataType:
        items = self.json["tables"]["items"]
        data = []
        
        for item in items:
            data.append({
                "id": item["id"],
                "filename": self.get_any_filename(
                    self.constrain_filename(
                        get_safe_filename(item["name"])
                    )
                ),
                "owner_id": item.get("owner"),
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

# TODO: Add celery tasks!
