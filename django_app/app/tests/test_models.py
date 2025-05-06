from django.test import TestCase
from .models import Event

class EventModelTest(TestCase):
    def test_event_creation(self):
        event = Event.objects.create(title="Test", date="2023-01-01", user_id=1)
        self.assertEqual(event.title, "Test")
