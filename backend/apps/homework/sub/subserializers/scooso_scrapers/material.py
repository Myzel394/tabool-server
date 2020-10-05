from rest_framework import serializers

from ....models import Material


class MaterialScoosoScraperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            ""
        ]
