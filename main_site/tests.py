from django.test import TestCase, RequestFactory
from main_site.views import main_resume
from main_site.models import Resume
from unittest.mock import patch


class MainResumeViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def successful_resume_request(self):
        with patch.object(Resume, 'objects') as mock_objects:
            mock_objects.first.return_value = Resume.objects.first()
            request = self.factory.get('/resume/')
            response = main_resume(request)
            self.assertEqual(response.status_code, 200)

    def no_resume_found_scenario(self):
        with patch.object(Resume, 'objects') as mock_objects:
            mock_objects.first.return_value = None
            request = self.factory.get('/resume/')
            response = main_resume(request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content, b'No resume found')
