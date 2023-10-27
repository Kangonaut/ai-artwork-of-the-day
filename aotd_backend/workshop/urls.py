from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()

# settings
router.register('user-settings', views.UserSettingsViewSet)
router.register('pushover-settings', views.PushoverSettingsViewSet)
router.register('open-weather-settings', views.OpenWeatherSettingsViewSet)
router.register('caldav-settings', views.CalDavSettingsViewSet)

router.register('artworks', views.ArtworkViewSet, basename='artwork')

urlpatterns = [
    path('hello-world/', views.hello_world),
    path('issue-artwork/', views.issue_artwork),
    path('artworks/me', views.PersonalArtworksView.as_view()),
    path('', include(router.urls)),
]
