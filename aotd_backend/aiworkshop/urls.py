from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('basic-config', views.BasicConfigView)

urlpatterns = [
    path('hello-world/', views.hello_world),
    path('issue-artwork/', views.issue_artwork),
    path('', include(router.urls)),
]
