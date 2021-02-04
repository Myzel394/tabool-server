from django_hint import RequestType
from rest_framework.decorators import api_view
from rest_framework.response import Response

# from apps.django.main.school_data.serializers import DetailTeacherSerializer
from .... import constants


@api_view(["GET"])
def contacts(request: RequestType):
    serializer_context = {
        "request": request
    }
    main_teacher = request.user.student.main_teacher
    class_level = request.user.student.class_level
    
    return Response({
        "illness_report_email": constants.CONTACT_MAIL_MAP[class_level],
        "main_teacher": None  # DetailTeacherSerializer(instance=main_teacher, context=serializer_context).data,
    })
