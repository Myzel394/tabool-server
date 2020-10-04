from private_storage.views import PrivateStorageDetailView

from ...models import Material

__all__ = [
    "MaterialDownloadView"
]


class MaterialDownloadView(PrivateStorageDetailView):
    model = Material
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return super().get_queryset().user_accessible(self.request.user)
        return None
    
    def can_access_file(self, _) -> bool:
        return True
