from pathlib import Path

from django.conf import settings
from private_storage.models import PrivateFile

from apps.django.main.homework.models import Material, Submission

__all__ = [
    "private_storage_access_check"
]

storage_models = [
    Material, Submission
]


def private_storage_access_check(private_file: PrivateFile) -> bool:
    user = private_file.request.user
    
    if not user.is_authenticated:
        return False
    
    relative_path = Path(private_file.full_path).relative_to(settings.MEDIA_ROOT)
    
    for model in storage_models:
        for instance in model.objects.only("file").filter(file=relative_path):
            if instance.can_user_access_file(user):
                return True
    
    return False
