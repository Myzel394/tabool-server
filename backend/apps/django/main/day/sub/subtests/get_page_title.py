from unittest.mock import Mock, patch

from apps.django.authentication.user.mixins import UserTestMixin


class GetPageTitleTest(UserTestMixin):
    valid_mock_title = "bla bla bla"
    valid_mock = Mock(
        text=f"<html><title>{valid_mock_title}</title></html>",
        status_code=200,
    )
    invalid_html_mock = Mock(
        text="banana",
        status_code=200
    )
    invalid_status_code_mock_status_code = 429
    invalid_status_code_mock = Mock(
        status_code=invalid_status_code_mock_status_code,
    )
    
    def setUp(self) -> None:
        self.Login_student()
    
    @patch("apps.django.main.day.sub.subviews.api.get_page_title.requests.Session.get")
    def test_get_valid(self, mock):
        mock.return_value = self.valid_mock
        
        response = self.client.get("/api/data/get-page-title/", {
            "url": "https://example.com"
        }, content_type="application/json")
        self.assertStatusOk(response.status_code)
        self.assertEqual(self.valid_mock_title, response.data["title"])
    
    @patch("apps.django.main.day.sub.subviews.api.get_page_title.requests.Session.get")
    def test_get_invalid_html(self, mock):
        mock.return_value = self.invalid_html_mock
        
        response = self.client.get("/api/data/get-page-title/", {
            "url": "https://example.com"
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
    
    @patch("apps.django.main.day.sub.subviews.api.get_page_title.requests.Session.get")
    def test_get_failed_status_code(self, mock):
        mock.return_value = self.invalid_status_code_mock
        
        response = self.client.get("/api/data/get-page-title/", {
            "url": "https://example.com"
        }, content_type="application/json")
        self.assertStatusNotOk(response.status_code)
        self.assertEqual(self.invalid_status_code_mock_status_code, response.data["proxy_status_code"])
