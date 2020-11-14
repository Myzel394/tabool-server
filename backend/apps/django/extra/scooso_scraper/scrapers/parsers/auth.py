from urllib.parse import parse_qs

from .base import BaseParser

__all__ = [
    "LoginParser"
]


class LoginParser(BaseParser):
    @property
    def data(self) -> dict:
        data = self.json["header"]["log"]
        auth_string = self.json["header"]["authString"]
        auth_data = parse_qs(auth_string)
        
        return {
            "id": data["id"],
            "first_name": data["prename"],
            "last_name": data["name"],
            "session": auth_data["logSessionId"][0],
            "second_session_data": auth_data["logUserIe"]
        }
    
    @property
    def is_valid(self) -> bool:
        try:
            return self.json["header"].get("log", None) is not None
        except:
            return False
