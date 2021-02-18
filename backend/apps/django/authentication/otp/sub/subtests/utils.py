from unittest.mock import Mock, patch

from django.test import TestCase

from apps.django.authentication.otp.utils import (
    get_ip_location, is_ip_geolocation_suspicious,
)


class OTPLocationUtilsTest(TestCase):
    mock = Mock(
        json=lambda: {
            "geo": {
                "latitude": 40.7128,
                "longitude": 74.0060
            },
            "name": "Uniteed States of America"
        },
        status_code=200,
    )
    not_suspicious_mock = Mock(
        json=lambda: {
            "geo": {
                "latitude": 7.472690,
                "longitude": 50.431960,
            },
            "name": "Germany"
        },
        status_code=200,
    )
    # Ip doesn't matter, request is mocked
    ip = "127.0.0.1"
    
    @patch("apps.django.authentication.otp.utils.requests.get")
    def test_get_ip_location(self, mock):
        mock.return_value = self.mock
        
        location = get_ip_location(self.ip)
        self.assertIsNotNone(location)
    
    @patch("apps.django.authentication.otp.utils.requests.get")
    def test_is_ip_geolocation_suspicious_is_suspicious(self, mock):
        mock.return_value = self.mock
        
        is_suspicious = is_ip_geolocation_suspicious(self.ip)
        self.assertTrue(is_suspicious)
    
    @patch("apps.django.authentication.otp.utils.requests.get")
    def test_is_ip_geolocation_suspicious_is_not_suspicious(self, mock):
        mock.return_value = self.not_suspicious_mock
        
        is_suspicious = is_ip_geolocation_suspicious(self.ip)
        self.assertFalse(is_suspicious)
