from pathlib import Path
from typing import *

from django.db import models
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.models.mixins import CreationDateMixin, RandomIDMixin
from django_lifecycle import (
    AFTER_CREATE, AFTER_DELETE, AFTER_UPDATE, BEFORE_UPDATE, hook,
    LifecycleModel,
)
from private_storage.fields import PrivateFileField

from apps.lesson.public import *
from . import SubmissionScoosoData
from ..exceptions import *
from ..public import build_submission_upload_to
from ..public.validators import safe_file_validator
from ..querysets import SubmissionQuerySet
from ...scooso_scraper.scrapers.material import MaterialRequest, MaterialTypeOptions
from ...scooso_scraper.scrapers.parsers.material import MaterialType
from ...utils import AssociatedUserMixin

if TYPE_CHECKING:
    from datetime import datetime
    from django.db.models.fields.files import FieldFile
    from apps.lesson.models import Lesson

__all__ = [
    "Submission"
]


class Submission(RandomIDMixin, AssociatedUserMixin, CreationDateMixin, LifecycleModel):
    class Meta:
        verbose_name = _("Einreichung")
        verbose_name_plural = _("Einreichungen")
        ordering = ("lesson", "upload_at")
    
    objects = SubmissionQuerySet.as_manager()
    
    lesson = models.ForeignKey(
        LESSON,
        verbose_name=lesson_single,
        on_delete=models.CASCADE,
    )  # type: Lesson
    
    file = PrivateFileField(
        verbose_name=_("Datei"),
        upload_to=build_submission_upload_to,
        max_length=1023,
        validators=[safe_file_validator]
    )  # type: FieldFile
    
    upload_at = models.DateTimeField(
        verbose_name=_("Hochladedatum"),
        help_text=_("Wann soll die Datei hochgeladen werden?"),
        blank=True,
        null=True
    )  # type: datetime
    
    is_uploaded = models.BooleanField(
        verbose_name=_("Hochgeladen?"),
        default=False
    )  # type: bool
    
    is_in_action = models.BooleanField(
        verbose_name=_("Wird hochgeladen"),
        help_text=_("Wenn ja, dann versucht der Server gerade die Datei hochzuladen."),
        default=False
    )  # type: bool
    
    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE, when="file")
    def _hook_get_scoosodata(self):
        material = self._get_material_from_scooso()
        self._create_material_from_scooso(material)
    
    @hook(BEFORE_UPDATE)
    def _hook_validate_upload_at_not_already_uploaded(self):
        if self.is_uploaded and self.has_changed("upload_at"):
            raise FileAlreadyUploadedError(_(
                "Die Datei wurde bereits am {upload_date} hochgeladen. Das Hochladedatum kann daher nicht mehr "
                "geändert werden."
            ), self.upload_at)
    
    @hook(AFTER_DELETE)
    def _hook_delete_file(self):
        Path(self.file.path).unlink(missing_ok=True)
        
        if self.is_uploaded:
            self.delete_file(False)
    
    def __str__(self):
        # Translators: Diese Nachricht ist für den Admin-Bereich. Sie wird verwendet, um Einreichungen darzustellen.
        return _("{filename} für {lesson} (Hochladedatum: {upload_date})").format(
            filename=self.file.name,
            lesson=self.lesson,
            upload_date=self.upload_at
        )
    
    def _get_material_from_scooso(self) -> MaterialType:
        user = self.associated_user
        
        with MaterialRequest(user.scoosodata.username, user.scoosodata.password) as scraper:
            materials = scraper.get_materials(
                time_id=self.lesson.lessonscoosodata.time_id,
                targeted_date=self.lesson.date,
                material_type=MaterialTypeOptions.HOMEWORK
            )
        
        materials = materials['materials']
        
        filename_materials = [
            material
            for material in materials
            if material['filename'] == Path(self.file.path).name
        ]
        if len(filename_materials) > 0:
            return filename_materials[0]
        return sorted(materials, key=lambda x: x['created_at'], reverse=True)[0]
    
    def _create_material_from_scooso(self, data: MaterialType) -> SubmissionScoosoData:
        scooso_data: SubmissionScoosoData
        scooso_data, _ = SubmissionScoosoData.objects.get_or_create(submission=self)
        scooso_data.scooso_id = data['scooso_id']
        scooso_data.save()
        
        return scooso_data
    
    def upload_file(self, commit: bool = True) -> None:
        if not self.is_in_action and not self.is_uploaded:
            self.is_in_action = True
            
            try:
                user = self.associated_user
                
                time_id = self.lesson.lessonscoosodata.time_id
                targeted_date = self.lesson.date
                filename = self.file.name
                content = Path(self.file.path).read_text()
                
                scraper = MaterialRequest(user.scoosodata.username, user.scoosodata.password)
                scraper.login()
                
                try:
                    scraper.upload_material(
                        time_id=time_id,
                        target_date=targeted_date,
                        filename=filename,
                        data=content,
                        material_type=MaterialTypeOptions.HOMEWORK
                    )
                except Exception as exception:
                    raise exception
                self.is_uploaded = True
            finally:
                self.is_in_action = False
                if commit:
                    self.save()
    
    def delete_file(self, commit: bool = True) -> None:
        if not self.is_in_action and self.is_uploaded:
            self.is_in_action = True
            
            try:
                user = self.associated_user
                file_id = self.submissionscoosodata.scooso_id
                
                scraper = MaterialRequest(user.scoosodata.username, user.scoosodata.password)
                scraper.login()
                
                try:
                    scraper.delete_material(file_id)
                except Exception as exception:
                    raise exception
                self.is_uploaded = False
            finally:
                self.is_in_action = False
                if commit:
                    self.save()
    
    @property
    def folder_name(self) -> str:
        return f"{self.lesson.lesson_data.course.folder_name}/{self.id}"
