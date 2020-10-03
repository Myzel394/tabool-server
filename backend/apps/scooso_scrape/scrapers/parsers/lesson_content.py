from datetime import datetime
from typing import *

from .base import BaseParser

__all__ = [
    "PureLessonContentParser", "PureLessonContentParserDataType"
]


class ContentType(TypedDict):
    presence: str
    online: str


class HomeworkType(TypedDict):
    information: str
    due_date: datetime


class PureLessonContentParserDataType(TypedDict):
    content: ContentType
    homework: HomeworkType


class PureLessonContentParser(BaseParser):
    @property
    def is_valid(self) -> bool:
        try:
            return type(self.json["item"]) is dict
        except KeyError:
            return False
    
    @property
    def data(self) -> PureLessonContentParserDataType:
        data = self.json["item"]
        
        return {
            "content": {
                "presence": data["topic_presence"],
                "online": data["topic_online"]
            },
            "homework": {
                "information": data["homework"],
                "due_date": data["homework_until"]
            }
        }
