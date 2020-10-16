from private_storage.views import PrivateStorageDetailView

from apps.homework.models import Material

__all__ = [
    "MaterialDownloadView"
]


class MaterialDownloadView(PrivateStorageDetailView):
    model = Material
    
    def can_access_file(self, private_file):
        return True
