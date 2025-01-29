from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import AnxietySurveyCreateViewSet

# Create a router and register the AnxietySurveyCreateViewSet with it
router = DefaultRouter()
router.register(r'anxiety-survey', AnxietySurveyCreateViewSet, basename='anxiety-survey')

urlpatterns = router.urls
