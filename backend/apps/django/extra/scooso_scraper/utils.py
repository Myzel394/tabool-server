import os
import re
import string
import unicodedata
from typing import *
from urllib import parse

from requests.utils import default_headers
from rest_framework import serializers

__all__ = [
    "build_url", "get_headers", "get_safe_filename", "get_mime_from_extension", "import_from_scraper",
    "rename_name_for_color_mapping"
]

from rest_framework.exceptions import ValidationError

VALID_FILENAME_CHARS = f"_-.() %s%s" % (string.ascii_letters, string.digits)
FILENAME_LENGTH_LIMIT = 255


def build_url(url: str, data: dict, suffix: str = "") -> str:
    return f"{url}?{parse.urlencode(data)}{suffix}"


def get_headers() -> dict:
    headers = default_headers()
    headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                            "Chrome/85.0.4183.102 Safari/537.36"
    
    return headers


def get_safe_filename(
        name: str,
        replacements: str = " ",
) -> str:
    for replacement in replacements:
        name = name.replace(replacement, "_")
    
    # Keep only valid ascii chars
    name = unicodedata.normalize("NFKD", name).encode("ASCII", "ignore").decode()
    
    # Keep only whitelisted chars
    name = "".join([
        char
        for char in name
        if char in VALID_FILENAME_CHARS
    ])
    
    return name[:FILENAME_LENGTH_LIMIT]


def get_mime_from_extension(filename):
    """Get mime type
    :param filename: str
    :type filename: str
    :rtype: str
    """
    mime_types = dict(
        txt='text/plain',
        htm='text/html',
        html='text/html',
        php='text/html',
        css='text/css',
        js='application/javascript',
        json='application/json',
        xml='application/xml',
        swf='application/x-shockwave-flash',
        flv='video/x-flv',
        
        # images
        png='image/png',
        jpe='image/jpeg',
        jpeg='image/jpeg',
        jpg='image/jpeg',
        gif='image/gif',
        bmp='image/bmp',
        ico='image/vnd.microsoft.icon',
        tiff='image/tiff',
        tif='image/tiff',
        svg='image/svg+xml',
        svgz='image/svg+xml',
        
        # archives
        zip='application/zip',
        rar='application/x-rar-compressed',
        exe='application/x-msdownload',
        msi='application/x-msdownload',
        cab='application/vnd.ms-cab-compressed',
        
        # audio/video
        mp3='audio/mpeg',
        ogg='audio/ogg',
        qt='video/quicktime',
        mov='video/quicktime',
        
        # adobe
        pdf='application/pdf',
        psd='image/vnd.adobe.photoshop',
        ai='application/postscript',
        eps='application/postscript',
        ps='application/postscript',
        
        # ms office
        doc='application/msword',
        rtf='application/rtf',
        xls='application/vnd.ms-excel',
        ppt='application/vnd.ms-powerpoint',
        
        # open office
        odt='application/vnd.oasis.opendocument.text',
        ods='application/vnd.oasis.opendocument.spreadsheet',
    )
    
    ext = os.path.splitext(filename)[1][1:].lower()
    if ext in mime_types:
        return mime_types[ext]
    else:
        return 'application/octet-stream'


def print_request(prepared):
    body = prepared.body.decode("ascii") if prepared.body else ""
    
    print('{}\n{}\r\n{}\r\n\r\n{}'.format(
        '-----------START-----------',
        prepared.method + ' ' + prepared.url,
        '\r\n'.join('{}: {}'.format(k, v) for k, v in prepared.headers.items()),
        body,
    ))


def import_from_scraper(
        serializer_class: Type[serializers.Serializer],
        data: dict,
        none_on_error: bool = False,
        **kwargs
):
    serializer = serializer_class(data=data)
    try:
        serializer.is_valid(True)
    except ValidationError as exception:
        if none_on_error:
            return None
        raise exception
    return serializer.save(**kwargs)


COlOR_MAPPING_RENAME_REGEX = re.compile(r"[ -]")


def rename_name_for_color_mapping(name: str) -> str:
    return COlOR_MAPPING_RENAME_REGEX.sub("_", name)
