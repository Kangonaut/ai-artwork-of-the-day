from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('user-settings', views.UserSettingsViewSet)
router.register('pushover-settings', views.PushoverSettingsViewSet)
router.register('open-weather-settings', views.OpenWeatherSettingsViewSet)

urlpatterns = [
    path('hello-world/', views.hello_world),
    path('issue-artwork/', views.issue_artwork),
    path('', include(router.urls)),
]
