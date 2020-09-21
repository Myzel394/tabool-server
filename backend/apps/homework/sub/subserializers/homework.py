from apps.utils.serializers import IdMixinSerializer


from ...models import Homework


class HomeworkSerializer(IdMixinSerializer):
    class Meta:
        model = Homework
        fields = ["lesson", "due_date", "information", "completed", "teacher", "id"]
    
    # TODO: Nested fields hinzufügen
