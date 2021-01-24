from django_hint import RequestType
from rest_framework.decorators import api_view
from rest_framework.response import Response

import constants
from apps.django.main.school_data.serializers import DetailTeacherSerializer


@api_view(["GET"])
def contacts(request: RequestType):
    return Response({
        "illness_report_email": constants.CONTACT_MAIL_MAP[request.user.student.class_level],
        "main_teacher": DetailTeacherSerializer(instance=request.user.student.main_teacher, context={
            "request": request
        }).data,
    })
