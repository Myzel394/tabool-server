import random
import string

from torrequest import TorRequest
from django.conf import settings
from requests import request
from typing import *

__all__ = [
    "generate_session"
]

DEFAULT_HEADERS = "Windows 10NT; Firefox 78.0.1"


def generate_session(user_agent_name: Optional[str] = None):
    if settings.IS_TOR:
        session = TorRequest().session
    else:
        session = request.Session()
    
    if user_agent_name:
        identifier = "".join(random.choices(string.ascii_letters + string.digits, k=20))
        user_agent = f"ScoosoScraper-{user_agent_name}-{identifier};"
    else:
        user_agent = DEFAULT_HEADERS
    
    session.headers.update({
        "User-Agent": user_agent
    })
    
    return session
    