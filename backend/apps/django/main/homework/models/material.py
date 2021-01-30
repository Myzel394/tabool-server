import mimetypes
import os
import re
from datetime import datetime
from pathlib import Path
from typing import *

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import RandomIDMixin
from django_common_utils.libraries.utils import listify, model_verbose
from django_lifecycle import AFTER_DELETE, BEFORE_CREATE, BEFORE_SAVE, BEFORE_UPDATE, hook, LifecycleModel
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
    
    _original_filename = models.CharField(
        verbose_name=_("Originaler Dateiname"),
        max_length=255,
        blank=True,
        null=True
    )
    
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
            if self._original_filename is None:
                raise ValidationError(_("Dateiname fehlt!"))
            
            self.name = self.improve_name(self._original_filename)
            
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
        return self.lesson.course.participants.only("id").filter(id=user.id).exists()
    
    @hook(AFTER_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)
    
    @hook(BEFORE_SAVE)
    def _hook_set_added_at(self):
        # Set added_at if it doesn't exists. (Probably because it was added via admin panel)
        self.added_at = self.added_at or datetime.now()
    
    @hook(BEFORE_CREATE)
    @hook(BEFORE_UPDATE, when_any=["name", "file"], has_changed=True)
    def _hook_full_clean(self):
        self.full_clean()
    
    @property
    def folder_name(self) -> str:
        return f"{self.lesson.course.folder_name}"
    
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
    
    def improve_name(self, name: str) -> str:
        improved_name = name
        
        # Remove prefixes
        # Remove "AB" and "AA"
        search = r"^(?i:(aa|ab))(?=[A-Z_])"
        improved_name = re.sub(search, "", improved_name)
        
        # Remove "lk" and "gk"
        search = "^(gk|lk)"
        improved_name = re.sub(search, "", improved_name, flags=re.IGNORECASE)
        
        # Remove unnecessary course name
        course = self.lesson.course
        course_name = re.escape(course.name)
        number_reversed_course_name = re.escape(
            f"{course.get_class_number()}{course.name}"
        )
        subject_name_short = re.escape(course.subject.short_name)
        searches = "|".join([course_name, subject_name_short, number_reversed_course_name])
        search = rf"^(?i:({searches}))(?![a-z])"
        improved_name = re.sub(search, "", improved_name)
        
        # Improve overall
        # Replace dashes with underscores
        improved_name = improved_name.replace("-", "_")
        
        # Remove start and end underscores
        improved_name = improved_name.lstrip("_").rstrip("_")
        
        # Strip underscore
        improved_name = re.sub(r"_+", "_", improved_name)
        
        # Replace underscores with spaces
        improved_name = improved_name.replace("_", " ")
        
        # Strip space
        improved_name = improved_name.strip()
        improved_name = re.sub(r"\s\s+", " ", improved_name)
        
        # Umlaute
        improved_name = improved_name.replace("ae", "ä").replace("ue", "ü").replace("oe", "ö")
        
        # Capitalize
        improved_name = improved_name.title()
        
        # Normalize file ending
        name, extension = os.path.splitext(improved_name)
        
        return f"{name}{extension.lower()}"
