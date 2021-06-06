from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from django_common_utils.libraries.fieldsets.mixins import DefaultAdminMixin

from .models import Choice, Poll
from .utils import get_results


class ChoiceInline(admin.TabularInline):
    model = Choice
    fields = [
        "text", "color"
    ]
    min_num = 2


@admin.register(Poll)
class PollAdmin(DefaultAdminMixin):
    fieldset_fields = {
        "default": ["title", "max_vote_date", "show_results_date", "targeted_user"],
        "extra": [["min_vote_choices", "max_vote_choices"]]
    }
    list_display = ["title", "max_vote_date", "show_results_date", "min_vote_choices", "max_vote_choices", "results"]
    search_fields = ["title"]
    date_hierarchy = "max_vote_date"
    filter_horizontal = ["targeted_user"]
    inlines = [ChoiceInline]

    @staticmethod
    def results(instance: Poll):
        poll_results = get_results(instance=instance)

        message = ""

        for result in poll_results:
            try:
                choice: Choice = Choice.objects.only("id").get(id=result["choice_id"])
            except ObjectDoesNotExist:
                return _("Fehler")

            value = result["percentage_value"]

            message += f"{choice.text}: {value * 100}%\n"

        message += f" ({instance.votes.count()} Stimmen)"

        return message

    results.short_description = _("Ergebnis")
