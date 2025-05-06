from django.contrib import admin
from .models import CalendarEvent, EventParticipation, UserStats

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'owner')
    list_filter = ('start_time', 'owner')
    search_fields = ('title', 'description')
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(owner=request.user)

@admin.register(EventParticipation)
class EventParticipationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'can_edit', 'created_at')
    list_filter = ('can_edit', 'created_at')

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'events_created', 'events_participated', 'last_active')
    readonly_fields = ('last_active',)
    
    def has_add_permission(self, request):
        return False
