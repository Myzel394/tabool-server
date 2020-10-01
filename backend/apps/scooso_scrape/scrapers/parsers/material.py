import string
import unicodedata
from datetime import datetime
from typing import *

from .base import BaseParser

__all__ = [
    "PureMaterialParser", "PureMaterialParserDataType"
]

VALID_FILENAME_CHARS = f"_-.() %s%s" % (string.ascii_letters, string.digits)
FILENAME_LENGTH_LIMIT = 255


class PureMaterialParserDataType(TypedDict):
    id: int
    filename: str
    owner: Optional[int]
    created_at: Optional[datetime]
    edited_at: Optional[datetime]


class PureMaterialParser(BaseParser):
    @staticmethod
    def get_safe_filename(
            name: str,
            replacements: str = " ",
    ) -> str:
        for replacement in replacements:
            name = name.replace(replacement, "_")
        
        # Keep only valid ascii chars
        name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode()
        
        # Keep only whitelisted chars
        name = "".join([
            char
            for char in name
            if char in VALID_FILENAME_CHARS
        ])
        
        return name[:FILENAME_LENGTH_LIMIT]
    
    @property
    def data(self) -> List[PureMaterialParserDataType]:
        items = self.json["tables"]["items"]
        data = []
        
        for item in items:
            data.append({
                "id": item["id"],
                "filename": self.get_safe_filename(item["name"]),
                "owner": item.get("owner"),
                "created_at": item.get("created"),
                "edited_at": item.get("edited"),
            })
        
        return data
    
    @property
    def is_valid(self) -> bool:
        try:
            return len(self.json["tables"]["items", []]) != 0
        except:
            return False
