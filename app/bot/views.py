from rest_framework import viewsets
from rest_framework.response import Response
from .models import Event, UserProfile
from .serializers import EventSerializer, UserProfileSerializer
import csv
from django.http import HttpResponse

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

def export_events(request, user_id):
    events = Event.objects.filter(organizer__userprofile__telegram_id=user_id)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="events_{user_id}.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Date', 'Status'])
    for event in events:
        writer.writerow([event.title, event.date, event.status])
    return response
