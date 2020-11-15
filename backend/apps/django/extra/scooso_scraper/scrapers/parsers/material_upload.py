from dataclasses import dataclass


@dataclass
class MaterialUploadParser:
    data: bytes
    
    @property
    def is_valid(self) -> bool:
        return True
