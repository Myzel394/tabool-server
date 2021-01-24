from rest_framework import serializers

from apps.django.main.homework.models import Submission


class SizeMixin(serializers.Serializer):
    size = serializers.SerializerMethodField()
    
    @staticmethod
    def get_size(instance: Submission):
        return instance.file.size
