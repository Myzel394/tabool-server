from private_storage.models import PrivateFile

__all__ = [
    "private_storage_access_check"
]


def private_storage_access_check(private_file: PrivateFile) -> bool:
    print("called private")
    return True
