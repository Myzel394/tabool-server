from simple_history.models import HistoricalRecords

from .models import UserInformationHistoricalModel

__all__ = [
    "set_user_information"
]


def set_user_information(history_instance: UserInformationHistoricalModel, **kwargs):
    thread = HistoricalRecords.thread
    
    if hasattr(thread, "request"):
        request = thread.request
        history_instance.ip_address = request.META["REMOTE_ADDR"]
