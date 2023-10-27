import abc

import django.db.models
import django.http as http
import rest_framework.serializers
from rest_framework import viewsets, mixins, status, exceptions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.views import APIView

import users.models
from . import models, serializers, tasks
from typing import Type


# Create your views here.
@api_view(['GET'])
def hello_world(request):
    return Response({'message': 'Hello World!'})


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def issue_artwork(request):
    tasks.generate_artwork.delay(request.user.id)

    return Response({
        'status': 'generation process started successfully',
    })


# class UserSettingsViewSet(viewsets.GenericViewSet):
#     permission_classes = [IsAuthenticated]
#     queryset = models.UserSettings.objects.all()
#     serializer_class = serializers.UserSettingsSerializer
#
#     @action(detail=False, methods=['GET', 'POST', 'PUT'])  # endpoint: 'user-settings/me'
#     def me(self, request):
#         user: models.CustomUser = request.user
#         user_settings, created = models.UserSettings.objects.get_or_create(user=user)
#
#         if request.method == 'GET':
#             serializer = serializers.UserSettingsSerializer(instance=user_settings)
#             return Response(serializer.data)
#
#         elif request.method == 'POST':
#             if created:
#                 serializer = serializers.UserSettingsSerializer(instance=user_settings, data=request.data)
#                 serializer.is_valid(raise_exception=True)
#                 serializer.save()
#                 return Response(serializer.data)
#             else:
#                 return Response({'detail': 'user-settings already exist for this user'},
#                                 status=status.HTTP_409_CONFLICT)
#
#         elif request.method == 'PUT':
#             serializer = serializers.UserSettingsSerializer(instance=user_settings, data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#             return Response(serializer.data)


class AbstractSettingsViewSet(abc.ABC, viewsets.GenericViewSet):
    settings_model: Type[django.db.models.Model] = None
    serializer_class: Type[rest_framework.serializers.ModelSerializer] = None
    queryset: django.db.models.QuerySet = None
    permission_classes = [IsAuthenticated]

    # detail = False -> URL does not contain instance pk
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


class UserSettingsViewSet(AbstractSettingsViewSet):
    settings_model = models.UserSettings
    serializer_class = serializers.UserSettingsSerializer
    queryset = models.UserSettings.objects.all()


class PushoverSettingsViewSet(AbstractSettingsViewSet):
    settings_model = models.PushoverSettings
    serializer_class = serializers.PushoverSettingsSerializer
    queryset = models.PushoverSettings.objects.all()


class OpenWeatherSettingsViewSet(AbstractSettingsViewSet):
    settings_model = models.OpenWeatherSettings
    serializer_class = serializers.OpenWeatherSettingsSerializer
    queryset = models.OpenWeatherSettings.objects.all()


class CalDavSettingsViewSet(AbstractSettingsViewSet):
    settings_model = models.CalDavSettings
    serializer_class = serializers.CalDavSettingsSerializer
    queryset = models.CalDavSettings.objects.all()


class PrivateArtworkViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = serializers.ArtworkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Artwork.objects.filter(
            user=self.request.user,
        ).order_by('-created_at')

    @action(detail=True, methods=['GET'])
    def image(self, request: Request, pk: int):
        artwork = self.get_queryset().get(pk=pk)
        return http.HttpResponse(artwork.image.file, content_type="image/png")
