from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import CalendarEvent, EventParticipation, UserStats
from .serializers import CalendarEventSerializer, EventParticipationSerializer, UserStatsSerializer

class CalendarEventViewSet(viewsets.ModelViewSet):
    queryset = CalendarEvent.objects.all()
    serializer_class = CalendarEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return CalendarEvent.objects.filter(owner=user) | CalendarEvent.objects.filter(participants=user)

class EventParticipationViewSet(viewsets.ModelViewSet):
    queryset = EventParticipation.objects.all()
    serializer_class = EventParticipationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class UserStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserStats.objects.all()
    serializer_class = UserStatsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
