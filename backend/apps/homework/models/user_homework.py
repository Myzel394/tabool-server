from django.utils.translation import gettext_lazy as _

from .mixins.homework import BaseHomeworkMixin
from ...utils.models import AddedAtMixin, AssociatedUserMixin
from ..querysets import UserHomeworkQuerySet


class UserHomework(BaseHomeworkMixin, AssociatedUserMixin):
    class Meta:
        verbose_name = _("Eigene Hausaufgabe")
        verbose_name_plural = _("Eigene Hausaufgaben")
        ordering = ("-completed", "due_date")

    objects = UserHomeworkQuerySet.as_manager()
