from dataclasses import dataclass


@dataclass
class MaterialUploadParser:
    content: bytes
    
    @property
    def is_valid(self) -> bool:
        # Content is always empty, so no method to check
        return True
    
    @property
    def data(self):
        return None
