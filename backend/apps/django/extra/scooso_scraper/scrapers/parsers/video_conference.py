from ..parsers import BaseParser


class VideoConferenceParser(BaseParser):
    @property
    def is_valid(self) -> bool:
        try:
            self.json["item"]["vlink"]
            return True
        except:
            return False
    
    @property
    def data(self):
        return self.json["item"]["vlink"]
