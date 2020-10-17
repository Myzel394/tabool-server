from django.contrib import admin
from django_common_utils.libraries.fieldsets.mixins import CreationDateAdminFieldsetMixin, DefaultAdminMixin

from apps.django.extra.scooso_scraper.mixins.admins import ScoosoDataAdminInlineMixin
from apps.django.main.school_data.public import model_verboses as school_verbose
from ...models import Submission, SubmissionScoosoData

__all__ = [
    "SubmissionAdmin"
]


class SubmissionScoosoDataAdminInline(ScoosoDataAdminInlineMixin):
    model = SubmissionScoosoData
    fieldset_fields = {
        "default": ["scooso_id"]
    }


@admin.register(Submission)
class SubmissionAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["lesson", "file", "upload_at", "is_uploaded", "!..."],
        "advanced": ["associated_user"]
    }
    autocomplete_fields = ["lesson"]
    list_filter = ["is_uploaded", "lesson__lesson_data__course", "lesson__lesson_data__course__subject"]
    list_display = ["lesson", "subject", "upload_at"]
    mixins = [CreationDateAdminFieldsetMixin]
    readonly_fields = ["is_uploaded"]
    inlines = [SubmissionScoosoDataAdminInline]
    
    def subject(self, instance: Submission):
        return instance.lesson.lesson_data.course.subject
    
    subject.short_description = school_verbose.SUBJECT
