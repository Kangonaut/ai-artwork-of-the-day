from django.urls import path, include
from . import views

urlpatterns = [
    path('hello-world/', views.hello_world),
]
