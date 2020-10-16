from django_common_utils.libraries.utils import model_verbose


def room_single():
    return model_verbose(ROOM)


def subject_single():
    return model_verbose(SUBJECT)


def teacher_single():
    return model_verbose(TEACHER)
