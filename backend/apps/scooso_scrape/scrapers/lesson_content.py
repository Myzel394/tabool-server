from datetime import datetime

from .parsers import PureLessonContentParser, PureLessonContentParserDataType
from .request import Request
from .. import constants
from ..utils import build_url

__all__ = [
    "HomeworkRequest"
]


class HomeworkRequest(Request):
    def get_homework(
            self,
            time_id: int,
            targeted_datetime: datetime
    ) -> PureLessonContentParserDataType:
        method = constants.LESSON_CONTENT_CONNECTION["method"]
        url = constants.LESSON_CONTENT_CONNECTION["url"]
        suffix = f"&pardate={targeted_datetime.strftime(constants.LESSON_CONTENT_CONNECTION['dt_format'])}"
        
        def get_data():
            data = {
                "cmd": 600,
                "subcmd": 200,
                "time_id": time_id,
                **self.login_data
            }
            
            return {
                "url": build_url(url, data) + suffix,
                "method": method
            }
        
        return self.request_with_parser(
            parser_class=PureLessonContentParser,
            get_data=get_data,
        )
