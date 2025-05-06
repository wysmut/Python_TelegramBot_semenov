from django.db import models
from django.contrib.auth.models import User

class CalendarEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_events')
    participants = models.ManyToManyField(User, through='EventParticipation', related_name='participating_events')
    
    def __str__(self):
        return self.title

class EventParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(CalendarEvent, on_delete=models.CASCADE)
    can_edit = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'event')

class UserStats(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    events_created = models.PositiveIntegerField(default=0)
    events_participated = models.PositiveIntegerField(default=0)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} stats"
