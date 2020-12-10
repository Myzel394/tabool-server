from django_hint import RequestType
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .... import constants


@api_view(["GET"])
def contacts(request: RequestType):
    return Response({
        "illness_report": constants.CONTACT_MAIL_MAP[request.user.student.class_level],
        "main_teacher": request.user.student.main_teacher.email
    })
