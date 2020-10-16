import mimetypes
from datetime import date
from enum import Enum
from pathlib import Path

from magic import Magic
from secure_file_detection import detector
from secure_file_detection.exceptions import *

from .parsers import PureMaterialParser
from .parsers.material import PureMaterialParserDataType
from .parsers.material_delete import MaterialDeleteParser
from .parsers.material_download import MaterialFileParser
from .parsers.material_upload import MaterialUploadParser
from .request import Request
from .. import constants
from ..exceptions import FileManipulatedException
from ..utils import build_url, get_mime_from_extension, get_safe_filename

__all__ = [
    "MaterialRequest", "MaterialTypeOptions"
]


class MaterialTypeOptions(Enum):
    TEACHER_MATERIALS = 310
    HOMEWORK = 320


class MaterialRequest(Request):
    magic = Magic(mime=True)
    
    @staticmethod
    def constrain_filename(file: Path) -> Path:
        true_type = detector.detect_true_type(file)
        extension = mimetypes.guess_extension(true_type, strict=True)
        
        return file.with_suffix(extension)
    
    @classmethod
    def create_file(cls, original_path: Path, data: bytes) -> Path:
        # Preparation
        mime_type = cls.magic.from_buffer(data)
        extension = mimetypes.guess_extension(mime_type, False)
        
        original_path = original_path.with_name(get_safe_filename(original_path.name))
        original_path = original_path.with_suffix(extension)
        original_path.parent.mkdir(exist_ok=True, parents=True)
        
        with original_path.open("wb") as file:
            file.write(data)
        
        # Validation
        try:
            true_type = detector.detect_true_type(original_path)
        except (ManipulatedFileError, MimeTypeNotSupported, MimeTypeNotDetectable):
            original_path.unlink()
            
            raise FileManipulatedException()
        
        extension = mimetypes.guess_extension(true_type)
        real_path = original_path.with_suffix(extension)
        
        original_path.rename(real_path)
        
        return original_path
    
    def get_materials(
            self,
            time_id: int,
            targeted_date: date,
            material_type: MaterialTypeOptions = MaterialTypeOptions.TEACHER_MATERIALS
    ) -> PureMaterialParserDataType:
        method = constants.MATERIAL_CONNECTION["method"]
        url = constants.MATERIAL_CONNECTION["url"]
        suffix = f"&pardate={targeted_date.strftime(constants.TIMETABLE_CONNECTION['dt_format'])}"
        
        def get_data():
            data = {
                "cmd": 4000,
                "subcmd": 5,
                "subsubcmd": 2,
                "prop": material_type.value,
                "destid": time_id,
                "desttype": 10030,
                **self.login_data
            }
            return {
                "url": build_url(url, data) + suffix,
                "method": method
            }
        
        return self.request_with_parser(
            parser_class=PureMaterialParser,
            get_data=get_data
        )
    
    def get_teacher_homework(
            self,
            time_id: int,
            targeted_date: date,
    ) -> PureMaterialParserDataType:
        return self.get_materials(
            time_id=time_id,
            targeted_date=targeted_date,
            material_type=MaterialTypeOptions.TEACHER_MATERIALS
        )
    
    def get_user_homework(
            self,
            time_id: int,
            targeted_date: date
    ) -> PureMaterialParserDataType:
        return self.get_materials(
            time_id=time_id,
            targeted_date=targeted_date,
            material_type=MaterialTypeOptions.HOMEWORK
        )
    
    def download_material(
            self,
            material_id: int,
            download_to: Path,
    ) -> Path:
        url = constants.MATERIAL_DOWNLOAD_CONNECTION["url"]
        suffix = f"&file[{int(material_id)}]=on"
        method = constants.MATERIAL_DOWNLOAD_CONNECTION["method"]
        
        def get_data():
            data = {
                "cmd": 3000,
                "subcmd": 20,
                "varname": "file",
                **self.login_data
            }
            return {
                "url": build_url(url, data) + suffix,
                "method": method
            }
        
        data = self.request_with_parser(
            parser_class=MaterialFileParser,
            get_data=get_data
        )
        
        return self.create_file(download_to, data)
    
    def upload_material(
            self,
            time_id: int,
            target_date: date,
            filename: str,
            data: str,
            material_type: MaterialTypeOptions = MaterialTypeOptions.HOMEWORK,
    ) -> None:
        url = constants.MATERIAL_UPLOAD_CONNECTION["url"]
        method = constants.MATERIAL_UPLOAD_CONNECTION["method"]
        targeted_date_str = target_date.strftime(constants.MATERIAL_UPLOAD_CONNECTION["dt_format"])
        mimetype_from_extension = get_mime_from_extension(filename)
        
        def get_data():
            form_data = {
                "cmd": 3000,
                "subcmd": 10,
                "dir": material_type.value,
                "destType": 10030,
                "destId": time_id,
                "parDate": targeted_date_str,
                **self.login_data
            }
            
            return {
                "url": url,
                "method": method,
                "files": {
                    "file": (filename, data, mimetype_from_extension)
                },
                "data": form_data
            }
        
        self.request_with_parser(
            parser_class=MaterialUploadParser,
            get_data=get_data
        )
    
    def delete_material(
            self,
            file_id: int
    ) -> None:
        url = constants.MATERIAL_UPLOAD_CONNECTION["url"]
        method = constants.MATERIAL_UPLOAD_CONNECTION["method"]
        
        def get_data():
            data = {
                "cmd": 3000,
                "subcmd": 30,
                "varname": "files",
                **self.login_data
            }
            suffix = f"&files[{file_id}]=on"
            
            return {
                "url": build_url(url, data) + suffix,
                "method": method
            }
        
        self.request_with_parser(
            parser_class=MaterialDeleteParser,
            get_data=get_data
        )
