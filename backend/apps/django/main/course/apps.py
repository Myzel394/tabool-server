from django.apps import AppConfig

from . import constants


class CourseConfig(AppConfig):
    name = 'apps.django.main.course'
    app_label = constants.APP_LABEL
