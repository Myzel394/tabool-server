import textwrap
from urllib.parse import urlencode

from django.conf import settings
from django.core.mail import send_mail
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    user = reset_password_token.user
    password_reset_link = instance.request.build_absolute_uri(
        f"/app/auth/forgot-password/confirm?" + urlencode({
            "token": reset_password_token.key,
            "email": user.email
        })
    )
    
    message = f"""
        Hallo {user.first_name}!
        
        Wenn du dein Passwort zurücksetzen möchtest, klicke auf diesen Link:
        
        {password_reset_link}
        
        Alternativ kannst du auch diesen Code eingeben:
        
        {reset_password_token.key}
        
        Wenn du nicht beantragt hast, dein Passwort zurücksetzen, dann ignoriere diese E-Mail einfach und gib diesen
        Code auf gar keinen Fall weiter! Der Code (und der Link) sind für eine Stunde gültig.
    """.strip()
    message = textwrap.dedent(message)
    
    send_mail(
        "Passwort zurücksetzen",
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
    )
