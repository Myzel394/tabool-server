from dataclasses import dataclass


@dataclass
class MaterialFileParser:
    data: str
    
    @property
    def is_valid(self) -> bool:
        return self.data != ""
