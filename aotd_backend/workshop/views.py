import abc
import json
from typing import Type

import django.db.models
import django.http as http
import rest_framework.serializers
from rest_framework import viewsets, mixins, status, exceptions, generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from . import models, serializers, tasks, permissions


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
    @action(detail=False, methods=['HEAD', 'GET', 'POST', 'PUT', 'DELETE'])
    def me(self, request: Request):
        user: models.CustomUser = request.user
        try:
            settings = self.settings_model.objects.get(user=user)
        except self.settings_model.DoesNotExist:
            settings = None

        if request.method in ['HEAD', 'GET', 'PUT', 'DELETE'] and settings is None:
            raise exceptions.NotFound(detail='does not exist for this user')

        if request.method == 'HEAD':
            return Response()

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


class DaytimeSettingsViewSet(AbstractSettingsViewSet):
    settings_model = models.DaytimeSettings
    serializer_class = serializers.DaytimeSettingsSerializer
    queryset = models.DaytimeSettings.objects.all()


class PrivateArtworkViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = serializers.PrivateArtworkSerializer
    permission_classes = [IsAuthenticated, permissions.IsOwner]

    def get_queryset(self):
        return models.Artwork.objects.filter(
            user=self.request.user,
        ).order_by('-created_at')

    @action(detail=True, methods=['GET'])
    def image(self, request: Request, pk: int):
        artwork = self.get_queryset().get(pk=pk)
        return http.HttpResponse(artwork.image.file, content_type="image/png")

    @action(detail=True, methods=["PUT"])
    def publish(self, request: Request, pk: int):
        # deserialize request data
        serializer = serializers.PublishArtworkSerializer(data=request.data)
        serializer.is_valid()
        is_public = serializer.data.get("publish")

        # get artwork
        artwork = models.Artwork.objects.get(pk=pk)

        # set visibility
        artwork.is_public = is_public
        artwork.save()

        # serialize artwork
        artwork_serializer = serializers.PrivateArtworkSerializer(instance=artwork)
        return Response(artwork_serializer.data)


class PublicArtworksViewSet(
    viewsets.GenericViewSet,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
):
    serializer_class = serializers.PublicArtworkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return models.Artwork.objects.filter(
            is_public=True,
        ).order_by('-created_at')

    @action(detail=True, methods=['GET'])
    def image(self, request: Request, pk: int):
        artwork = self.get_queryset().get(pk=pk)
        return http.HttpResponse(artwork.image.file, content_type="image/png")


# list view for available art styles

class ArtStyleViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin
):
    queryset = models.ArtStyle.objects.all()
    serializer_class = serializers.ArtStyleSerializer


class ArtStyleSettingsViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["GET", "PUT"])
    def me(self, request: Request) -> Response:
        user: models.CustomUser = request.user
        art_style_queryset = user.artstyle_set.all()

        if request.method == "GET":
            art_style_pks = [art_style.id for art_style in art_style_queryset]
            return Response({
                "art_styles": art_style_pks,
            })

        if request.method == "PUT":
            # retrieve request body
            if "art_styles" not in request.data:
                return Response({"art_styles": "required field"}, status.HTTP_400_BAD_REQUEST)
            art_style_pks: list[int] = request.data["art_styles"]

            # delete previous art-styles
            for art_style in art_style_queryset:
                art_style.users.remove(user)

            # insert new art-styles
            print(art_style_pks)
            for art_style_pk in art_style_pks:
                models.ArtStyle.objects.get(pk=art_style_pk).users.add(user)

            return Response({
                "art_styles": art_style_pks,
            })
