import json
from dataclasses import dataclass


@dataclass
class MaterialUploadParser:
    response_data: bytes
    
    @property
    def is_valid(self) -> bool:
        try:
            data = self.response_data.decode('ascii')
            json.loads(data)["item"]["file_id"]
            return True
        except:
            return False
    
    @property
    def data(self):
        data = self.response_data.decode('ascii')
        return json.loads(data)["item"]["file_id"]
