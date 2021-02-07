from typing import *

from django.db.models import QuerySet
from django_hint import QueryType
from fcm_django.models import FCMDevice, FCMDeviceQuerySet

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User


def get_as_list(value) -> list:
    if type(value) is list:
        return value
    elif isinstance(value, QuerySet):
        return value
    return value


def send_notification(
        users: Union[list["User"], "User", QueryType["User"]],
        title: str,
        body: Optional[str] = None,
        data: Optional[Any] = None,
        collapse_group_name: Optional[str] = None,
        is_important: bool = False,
        max_retry_time: int = 60
) -> None:
    users = get_as_list(users)
    
    devices: FCMDeviceQuerySet = FCMDevice.objects.only("user").filter(user__in=users)
    
    # Bulk not working
    for device in devices:
        device.send_message(
            title=title,
            body=body,
            data=data,
            collapse_key=collapse_group_name,
            low_priority=not is_important,
            time_to_live=max(max_retry_time, 60),
        )
