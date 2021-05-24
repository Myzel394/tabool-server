from datetime import datetime
from pathlib import Path
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import BEFORE_CREATE, BEFORE_DELETE, BEFORE_SAVE, BEFORE_UPDATE, hook
from private_storage.fields import PrivateFileField

from apps.django.main.timetable.mixins import LessonMixin
from ..file_uploads import build_material_upload_to
from ..public import model_names
from ..querysets import MaterialQuerySet
from ..validators import only_future

if TYPE_CHECKING:
    from apps.django.authentication.user.models import User
    from django.db.models.fields.files import FieldFile

__all__ = [
    "Material"
]


class Material(RandomIDMixin, LessonMixin, CreationDateMixin):
    class Meta:
        verbose_name = model_names.MATERIAL
        verbose_name_plural = model_names.MATERIAL_PLURAL
        ordering = ("name", "publish_datetime", "created_at")
    
    objects = MaterialQuerySet.as_manager()
    
    name = models.CharField(
        verbose_name=_("Name"),
        max_length=31,
        blank=True,
    )
    
    publish_datetime = models.DateTimeField(
        verbose_name=_("Veröffentlichkeitsdatum"),
        help_text=_("Ab wann Schüler auf die Datei zugreifen können"),
        validators=[only_future],
    )
    
    announce = models.BooleanField(
        verbose_name=_("Ankündigen"),
        help_text=_("Kann aktiviert werden, wenn die Datei zu einem bestimmten Zeitpunkt veröffentlicht wird und die "
                    "Schüler vorher davon erfahren dürfen."),
        default=True,
    )
    
    file = PrivateFileField(
        verbose_name=_("Datei"),
        upload_to=build_material_upload_to,
        max_length=1023,
    )  # type: FieldFile
    
    def can_user_access_file(self, user: "User") -> bool:
        if user.is_student:
            if not self.publish_datetime < datetime.now():
                return False
            
            return self.lesson.course.participants.only("id").filter(user__id=user.id).exists()
        return self.lesson.course.teacher.user == user
    
    @property
    def folder_name(self) -> str:
        return f"{self.lesson.course.folder_name}"
    
    @hook(BEFORE_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when_any=["publish_datetime", "announce"], has_changed=True)
    def _hook_set_announce(self):
        self.full_clean()
        
        if not self.publish_datetime:
            self.announce = False
    
    @hook(BEFORE_SAVE)
    def _hook_autofill_name(self):
        if not self.name or self.name == "":
            self.name = Path(self.file.path).name
