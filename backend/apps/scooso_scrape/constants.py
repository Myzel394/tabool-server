BASE_URL = "https://scooso.org"
DEFAULT_QUERY_URL = f"{BASE_URL}/scooso/bin/php/query.php"

LOGIN_CONNECTION = {
    "url": f"{BASE_URL}/scooso/bin/m_index.php",
    "method": "POST"
}

TIMETABLE_CONNECTION = {
    "url": DEFAULT_QUERY_URL,
    "method": "POST",
    "dt_format": "%Y-%m-%d 00:00:00"
}

MATERIAL_CONNECTION = {
    "url": DEFAULT_QUERY_URL,
    "method": "POST"
}

MATERIAL_DOWNLOAD_CONNECTION = {
    "url": DEFAULT_QUERY_URL,
    "method": "GET"
}

MATERIAL_UPLOAD_CONNECTION = {
    "url": DEFAULT_QUERY_URL,
    "method": "POST",
    "dt_format": "%Y-%m-%d 00:00:00"
}

LESSON_CONTENT_CONNECTION = {
    "url": DEFAULT_QUERY_URL,
    "method": "POST",
    "dt_format": "%Y-%m-%d %H:%M:%S"
}
