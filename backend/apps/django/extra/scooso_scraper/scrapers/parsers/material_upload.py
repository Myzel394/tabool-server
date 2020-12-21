import json
from dataclasses import dataclass


@dataclass
class MaterialUploadParser:
    content: bytes
    
    @property
    def is_valid(self) -> bool:
        try:
            json.loads(self.content.decode("ascii"))["item"]["file_id"]
            return True
        except:
            return False
    
    @property
    def data(self):
        return json.loads(self.content.decode("ascii"))
