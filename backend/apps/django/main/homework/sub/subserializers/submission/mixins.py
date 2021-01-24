from pathlib import Path

from rest_framework import serializers

from apps.django.main.homework.models import Submission


class FilenameMixin(serializers.Serializer):
    filename = serializers.SerializerMethodField()
    
    @staticmethod
    def get_filename(instance: Submission):
        return Path(instance.file.path).name
