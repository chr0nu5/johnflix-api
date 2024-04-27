import json

from .views import BlankView
from django.test import RequestFactory
from django.test import TestCase


class BlankViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_request(self):
        request = self.factory.get('/blank/')
        response = BlankView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{}')

    def test_post_request_with_valid_json(self):
        request = self.factory.post(
            '/blank/', json.dumps({}), content_type='application/json')
        response = BlankView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'{}')

    def test_post_request_with_invalid_json(self):
        request = self.factory.post(
            '/blank/', 'invalid json', content_type='application/json')
        response = BlankView.as_view()(request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content),
                         {"error": "Invalid data"})
