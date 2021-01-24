from .base import BaseTeacherSerializer

__all__ = [
    "DetailTeacherSerializer"
]


class DetailTeacherSerializer(BaseTeacherSerializer):
    class Meta(BaseTeacherSerializer.Meta):
        fields = [
            "first_name", "last_name", "short_name", "email", "gender", "id"
        ]
