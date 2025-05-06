from django.contrib import admin
from .models import Event, BotStatistics, UserProfile

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'organizer', 'status')
    list_filter = ('status', 'is_public')
    search_fields = ('title', 'organizer__username')

@admin.register(BotStatistics)
class BotStatisticsAdmin(admin.ModelAdmin):
    list_display = ('event_count', 'user_interactions', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_id', 'name')
    search_fields = ('name', 'telegram_id')
