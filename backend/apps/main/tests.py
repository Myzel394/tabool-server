import smtplib

from django.core.mail import EmailMessage
from django.test import TestCase


class EmailTest(TestCase):
    def test_smtp(self):
        port = 1025
        smtp_server = "127.0.0.1"
        sender_email = "sender@mail.com"
        receiver_email = "to@mail.com"
        message = """
        Subject: Hi there
        
        This message is sent from Python."""
        
        with smtplib.SMTP(smtp_server, port) as server:
            server.sendmail(sender_email, receiver_email, message)
    
    def test_sending(self):
        email = EmailMessage('Hello', 'World', to=['user@gmail.com'])
        email.send()
