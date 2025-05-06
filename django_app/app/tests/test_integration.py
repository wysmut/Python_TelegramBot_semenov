from django.test import TestCase
from .models import Event

class IntegrationTest(TestCase):
    def test_full_flow(self):
        event = Event.objects.create(title="Test", date="2023-01-01", user_id=1)
        self.assertEqual(Event.objects.count(), 1)
