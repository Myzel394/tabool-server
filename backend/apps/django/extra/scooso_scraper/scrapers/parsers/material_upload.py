import json
from dataclasses import dataclass


@dataclass
class MaterialUploadParser:
    data: str
    
    @property
    def is_valid(self) -> bool:
        try:
            json.loads(self.data)["item"]["file_id"]
            return True
        except:
            return False
    
    @property
    def data(self):
        return json.loads(self.data)["item"]["file_id"]
