from django_common_utils.libraries.handlers.mixins import BaseHandlerMixin
from django_common_utils.libraries.utils import ensure_iteration
from rest_framework import serializers

from apps.django.main.homework.models import Homework

__all__ = [
    "HomeworkScoosoScraperSerializer"
]


class HomeworkScoosoScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = [
            "information", "due_date"
        ]
    
    def create(self, validated_data):
        handlers = Homework.handlers()["information"]
        information = validated_data.pop("information")
        for handler in ensure_iteration(handlers, lambda element: issubclass(element.__class__, BaseHandlerMixin)):
            information = handler.handle(information)
        
        return Homework.objects.get_or_create(
            lesson=validated_data["lesson"],
            due_date=validated_data["due_date"],
            information=information
        )[0]
