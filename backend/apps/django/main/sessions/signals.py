from django.db.models.signals import post_save
from django.dispatch import receiver
from user_sessions.models import Session

from apps.django.main.sessions.models import SessionRelation


@receiver(post_save, sender=Session)
def create_session_relation(instance: Session, created: bool, **kwargs):
    if created:
        SessionRelation.objects.create(
            session=instance
        )
