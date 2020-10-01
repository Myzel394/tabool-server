import os
import random
import stat
import string
from datetime import datetime, timedelta
from pathlib import Path
from typing import *

from .parsers import PureMaterialParser, PureMaterialParserDataType
from .parsers.material_file import MaterialFileParser
from .request import build_url, Request
from .. import constants

__all__ = [
    "MaterialRequest"
]


class MaterialRequest(Request):
    @staticmethod
    def get_pardate() -> datetime:
        return datetime.now() + timedelta(weeks=1) + random.choice([
            timedelta(days=days)
            for days in [0, 1, 3, 5, 7]
        ])
    
    @staticmethod
    def get_subfolder_path(base_path: Path) -> Path:
        suffix = f"{datetime.now().strftime('%d.%m.%y.%h.%M.%S')}__{''.join(random.choices(string.ascii_letters, k=4))}"
        path = base_path / suffix
        path.mkdir(parents=True, exist_ok=True)
        
        return path
    
    def get_materials(
            self,
            destination_id: int,
            calendar_id: int = 310,
    ) -> List[PureMaterialParserDataType]:
        url = constants.MATERIAL_CONNECTION["url"]
        data = {
            "cmd": 4000,
            "subcmd": 5,
            "subsubcmd": 2,
            "prop": calendar_id,
            "destid": destination_id,
            "desttype": 10030,
            **self.login_data
        }
        prefix = f"&pardate={self.get_pardate().strftime(constants.TIMETABLE_CONNECTION['dt_format'])}"
        
        full_url = build_url(url, data) + prefix
        
        return self.request_with_parser(
            parser_class=PureMaterialParser,
            method=constants.MATERIAL_CONNECTION["method"],
            full_url=full_url
        )
    
    def download_material(
            self,
            material_id: int,
            download_to: Path
    ) -> None:
        url = constants.MATERIAL_DOWNLOAD_CONNECTION["url"]
        data = {
            "cmd": 3000,
            "subcmd": 20,
            "varname": "file",
            **self.login_data
        }
        prefix = f"&file[{int(material_id)}]=on"
        
        full_url = build_url(url, data) + prefix
        
        data = self.request_with_parser(
            parser_class=MaterialFileParser,
            method=constants.MATERIAL_DOWNLOAD_CONNECTION["method"],
            full_url=full_url
        )
        
        with download_to.open("w", encoding="utf-8") as file:
            file.write(data)
        
        os.chmod(str(download_to), stat.S_IRGRP)
