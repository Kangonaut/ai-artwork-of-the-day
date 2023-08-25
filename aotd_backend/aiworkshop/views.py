from django.shortcuts import render
from rest_framework import viewsets, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . import models, serializers
import openai


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

    return Response({'status': 'successful'})


class BasicConfigView(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
):
    queryset = models.BasicConfig.objects.all()
    serializer_class = serializers.BasicConfigSerializer
