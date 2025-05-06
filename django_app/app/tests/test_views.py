from django.test import TestCase
from django.urls import reverse
from .models import Event

class EventViewTest(TestCase):
    def test_event_list(self):
        response = self.client.get(reverse('event-list'))
        self.assertEqual(response.status_code, 200)
