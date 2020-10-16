from ..parsers import BaseParser


class MaterialDeleteParser(BaseParser):
    @property
    def is_valid(self) -> bool:
        try:
            return self.json["header"]["logType"] == 20
        except:
            return False
    
    @property
    def data(self):
        return self.json
