from datetime import datetime

from .parsers import PureLessonContentParser, PureLessonContentParserDataType
from .request import Request
from .. import constants
from ..utils import build_url

__all__ = [
    "HomeworkRequest"
]


class HomeworkRequest(Request):
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
