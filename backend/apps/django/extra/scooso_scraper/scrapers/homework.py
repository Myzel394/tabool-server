from datetime import datetime
from typing import *

from apps.django.main.homework.models import Homework
from apps.django.main.homework.sub.subserializers import HomeworkScoosoScraperSerializer
from .parsers import PureLessonContentParser, PureLessonContentParserDataType
from .parsers.lesson_content import HomeworkType
from .request import Request
from .. import constants
from ..utils import build_url, import_from_scraper

if TYPE_CHECKING:
    from apps.django.main.lesson.models import Lesson

__all__ = [
    "LessonContentRequest"
]


class LessonContentRequest(Request):
    def build_get_homework_url(
            self,
            time_id: int,
            targeted_datetime: datetime
    ) -> str:
        url = constants.LESSON_CONTENT_CONNECTION["url"]
        data = {
            "cmd": 600,
            "subcmd": 200,
            "time_id": time_id,
            **self.login_data
        }
        suffix = f"&pardate={targeted_datetime.strftime(constants.LESSON_CONTENT_CONNECTION['dt_format'])}"
        
        return build_url(url, data) + suffix
    
    def get_homework(
            self,
            time_id: int,
            targeted_datetime: datetime
    ) -> PureLessonContentParserDataType:
        return self.request_with_parser(
            parser_class=PureLessonContentParser,
            get_data=lambda: {
                "url": self.build_get_homework_url(time_id=time_id, targeted_datetime=targeted_datetime),
                "method": constants.LESSON_CONTENT_CONNECTION["method"]
            },
        )
    
    @staticmethod
    def import_homework_from_scraper(
            data: HomeworkType,
            lesson: "Lesson"
    ) -> Homework:
        return import_from_scraper(HomeworkScoosoScraperSerializer, data, lesson=lesson)
