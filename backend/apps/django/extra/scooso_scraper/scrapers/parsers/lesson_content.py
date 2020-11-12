import base64
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
    ENCODING_TYPE = "utf-8"
    
    @property
    def is_valid(self) -> bool:
        try:
            return type(self.json["item"]) is dict
        except:
            return False
    
    @property
    def data(self) -> PureLessonContentParserDataType:
        data = self.json["item"]
        topic_online = data["topic_online_b64"]
        topic_presence = data["topic_presence_b64"]
        homework = data["homework_b64"]
        
        return {
            "content": {
                "presence": base64.b64decode(topic_presence).decode(self.ENCODING_TYPE) if topic_presence else None,
                "online": base64.b64decode(topic_online).decode(self.ENCODING_TYPE) if topic_online else None,
            },
            "homework": {
                "information": base64.b64decode(homework).decode(self.ENCODING_TYPE) if homework else None,
                "due_date": data["homework_until"]
            }
        }
