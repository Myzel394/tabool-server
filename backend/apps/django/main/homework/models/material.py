import mimetypes
from pathlib import Path
from typing import *

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_common_utils.libraries.utils import listify, model_verbose
from django_lifecycle import AFTER_DELETE, BEFORE_CREATE, BEFORE_UPDATE, hook, LifecycleModel
from magic import Magic
from private_storage.fields import PrivateFileField

from apps.django.main.lesson.public import *
from apps.django.main.lesson.public import model_names as lesson_names
from apps.django.utils.models import AddedAtMixin
from ..public import *
from ..public import model_names
from ..public.validators import safe_file_validator
from ..querysets import MaterialQuerySet

if TYPE_CHECKING:
    from apps.django.main.authentication.models import User

if TYPE_CHECKING:
    from apps.django.main.lesson.models import Lesson
    from django.db.models.fields.files import FieldFile


class Material(RandomIDMixin, AddedAtMixin, LifecycleModel):
    class Meta:
        verbose_name = model_names.MATERIAL
        verbose_name_plural = model_names.MATERIAL_PLURAL
        ordering = ("is_deleted", "-added_at", "name")
    
    objects = MaterialQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        on_delete=models.CASCADE,
        verbose_name=lesson_names.LESSON
    )  # type: Lesson
    
    file = PrivateFileField(
        verbose_name=_("Datei"),
        blank=True,
        null=True,
        upload_to=build_material_upload_to,
        max_length=1023,
    )  # type: FieldFile
    
    name = models.CharField(
        verbose_name=_("Dateiname"),
        max_length=255,
        blank=True,
        null=True
    )  # type: str
    
    is_deleted = models.BooleanField(
        verbose_name=_("Gelöscht"),
        default=False,
    )
    
    def __str__(self):
        return _("{material_model_verbose} {name} für {lesson}").format(
            material_model_verbose=model_verbose(self),
            name=self.name,
            lesson=self.lesson
        )
    
    def clean(self):
        if self.file.name is not None:
            if self.name is None:
                raise ValidationError(_("Dateiname fehlt!"))
            
            # Validate name extension
            m = Magic(mime=True)
            mimetype = m.from_buffer(self.file.open().read())
            extensions = mimetypes.guess_all_extensions(mimetype, strict=False)
            
            extension = Path(self.name).suffix
            
            if extension not in extensions:
                raise ValidationError(_(
                    'Die Endung "{extension}" im angegebenen Dateinamen ist für die hochgeladene Datei nicht gültig. '
                    'Wähle aus zwischen: {available_extensions}.'
                ).format(
                    extension=extension,
                    available_extensions=listify(extensions)
                ))
            
            safe_file_validator(self.file)
        
        return super().clean()
    
    def can_user_access_file(self, user: "User") -> bool:
        return self.lesson.lesson_data.course.participants.only("id").filter(id=user.id).exists()
    
    @hook(AFTER_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when_any=["name", "file"], has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @property
    def folder_name(self) -> str:
        return f"{self.lesson.lesson_data.course.folder_name}"
    
    @property
    def is_downloaded(self) -> bool:
        if not self.file:
            return False
        
        full_path = settings.MEDIA_ROOT / self.file.path
        
        return full_path.exists()
    
    def get_scooso_download_link(self, user: "User") -> Optional[str]:
        if scooso_data := getattr(self, "materialscoosodata", None):
            url = scooso_data.build_download_url(user)
            return url
        return
    
    def mark_as_deleted(self):
        self.is_deleted = True
        self.save()
