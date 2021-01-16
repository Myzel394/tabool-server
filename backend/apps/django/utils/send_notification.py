from typing import *

from fcm_django.models import FCMDevice, FCMDeviceQuerySet

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User


def send_notification(
        users: Union[list["User"], "User"],
        title: str,
        body: Optional[str] = None,
        data: Optional[Any] = None,
        collapse_group_name: Optional[str] = None,
        is_important: bool = False,
) -> None:
    users = users if type(users) is list else [users]
    
    devices: FCMDeviceQuerySet = FCMDevice.objects.only("user").filter(user__in=users)
    
    # Bulk not working
    for device in devices:
        device.send_message(
            title=title,
            body=body,
            data=data,
            collapse_key=collapse_group_name,
            low_priority=not is_important,
        )
