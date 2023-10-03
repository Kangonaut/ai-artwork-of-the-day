import time

from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers, signals, tasks
import openai
import json
import os


class ConfigManager:
    def update(self, key: str, value: str):
        pass

    def get(self, key: str) -> str:
        pass


# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello World!'})


@api_view(['GET'])
def issue_artwork(request):
    tasks.generate_artwork.delay()

    return Response({
        'status': 'request submitted successfully',
    })
