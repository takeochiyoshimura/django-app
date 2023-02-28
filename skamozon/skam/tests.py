
from django.test import TestCase, Client
from django.urls import reverse


class BlogTest(TestCase):
    def test_should_respond_only_for_example_a(self):
        client = Client(HTTP_HOST="127.0.0.1")
        view = reverse("index")
        response = client.get(view)
        self.assertEqual(response.status_code, 200)

    def test_should_not_respond_for_example_b(self):
        client = Client(HTTP_HOST="www.example-b.dev")
        view = reverse("index")
        response = client.get(view)
        self.assertEqual(response.status_code, 404)

    def test_should_not_respond_for_example_c(self):
        client = Client(HTTP_HOST="www.example-c.dev")
        view = reverse("index")
        response = client.get(view)
        self.assertEqual(response.status_code, 404)