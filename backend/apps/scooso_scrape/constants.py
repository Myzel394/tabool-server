BASE_URL = "https://scooso.org"

LOGIN_CONNECTION = {
    "url": f"{BASE_URL}/query_m.php",
    "method": "POST"
}

TIMETABLE_CONNECTION = {
    "url": f"{BASE_URL}/query.php",
    "method": "POST",
    "dt_format": "%Y-%M-YD 00:00:00"
}
