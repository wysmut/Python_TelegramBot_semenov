from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EventViewSet, UserProfileViewSet, export_events

router = DefaultRouter()
router.register(r'events', EventViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('export/<str:user_id>/', export_events, name='export_events'),
]
