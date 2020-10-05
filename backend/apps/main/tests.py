import smtplib

from django.core.mail import send_mail
from django.test import override_settings, TestCase


class EmailTest(TestCase):
    def test_smtp(self):
        # WORKS
        port = 1025
        smtp_server = "127.0.0.1"
        sender_email = "sender@mail.com"
        receiver_email = "to@mail.com"
        message = """
        Subject: Hi there
        
        This message is sent from Python."""
        
        with smtplib.SMTP(smtp_server, port) as server:
            server.sendmail(sender_email, receiver_email, message)
    
    @override_settings(EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend")
    def test_sending(self):
        # DOESNT WORK
        send_mail(
            'Subject here',
            'Here is the message.',
            'from@example.com',
            ['to@example.com'],
            fail_silently=False
        )
