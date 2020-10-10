from apps.utils.serializers import RandomIDSerializerMixin

from ...models import Submission


class SubmissionDetailSerializer(RandomIDSerializerMixin):
    class Meta:
        model = Submission
        fields = [
            "lesson", "file", ""
        ]
