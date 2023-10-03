from django.urls import path, include
from . import views

urlpatterns = [
    path('register-dummy/', views.register_dummy),
]
