import abc

import django.db.models
import rest_framework.serializers
from rest_framework import viewsets, mixins, status, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from . import models, serializers, tasks


# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello World!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def issue_artwork(request):
    tasks.generate_artwork.delay(request.user.id)

    return Response({
        'status': 'request submitted successfully',
    })


class UserSettingsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.UserSettings.objects.all()
    serializer_class = serializers.UserSettingsSerializer

    @action(detail=False, methods=['GET', 'POST', 'PUT'])  # endpoint: 'user-settings/me'
    def me(self, request):
        user: models.CustomUser = request.user
        user_settings, created = models.UserSettings.objects.get_or_create(user=user)

        if request.method == 'GET':
            serializer = serializers.UserSettingsSerializer(instance=user_settings)
            return Response(serializer.data)

        elif request.method == 'POST':
            if created:
                serializer = serializers.UserSettingsSerializer(instance=user_settings, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'detail': 'user-settings already exist for this user'},
                                status=status.HTTP_409_CONFLICT)

        elif request.method == 'PUT':
            serializer = serializers.UserSettingsSerializer(instance=user_settings, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class _DeliveryServiceSettingsViewSet(viewsets.GenericViewSet):
    settings_model: django.db.models.Model.__class__ = None
    serializer_class: rest_framework.serializers.ModelSerializer.__class__ = None
    queryset: django.db.models.QuerySet = None
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'POST', 'PUT', 'DELETE'])
    def me(self, request: Request):
        user: models.CustomUser = request.user
        try:
            settings = self.settings_model.objects.get(user=user)
        except self.settings_model.DoesNotExist:
            settings = None

        if request.method in ['GET', 'PUT', 'DELETE'] and settings is None:
            raise exceptions.NotFound(detail='does not exist for this user')

        if request.method == 'GET':
            serializer = self.serializer_class(instance=settings)
            return Response(serializer.data)

        elif request.method == 'POST':
            if settings is not None:
                return Response({'detail': 'already exist for this user'},
                                status=status.HTTP_409_CONFLICT)
            settings = self.settings_model(user=user)
            serializer = self.serializer_class(instance=settings, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = self.serializer_class(instance=settings, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            settings.delete()
            return Response({'detail': 'successfully deleted'}, status=status.HTTP_204_NO_CONTENT)


class PushoverSettingsViewSet(_DeliveryServiceSettingsViewSet):
    settings_model = models.PushoverSettings
    serializer_class = serializers.PushoverSettingsSerializer
    queryset = models.PushoverSettings.objects.all()
