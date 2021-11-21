from django.test import TestCase, SimpleTestCase, override_settings
from django.urls import reverse
from . import views

# Create your tests here.
class PageOpen(TestCase):
    def test_about_page_exist(self):
        url = reverse('about')
        r = self.client.get(url)
        self.assertEqual(r.status_code, 200)

@override_settings(ROOT_URLCONF=views)
class CustomErrorHandlerTests(SimpleTestCase):
    def test_handler_renders(self):
        response = self.client.get('/403/')
        self.assertContains(response, 'Error handler content', status_code=403)