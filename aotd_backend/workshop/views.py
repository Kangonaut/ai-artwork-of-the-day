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


class PushoverSettingsViewSet(viewsets.GenericViewSet):
    queryset = models.PushoverSettings.objects.all()
    serializer_class = serializers.PushoverSettingsSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['GET', 'POST', 'PUT', 'DELETE'])
    def me(self, request: Request):
        user: models.CustomUser = request.user
        try:
            pushover_settings = models.PushoverSettings.objects.get(user=user)
        except models.PushoverSettings.DoesNotExist:
            pushover_settings = None

        if request.method in ['GET', 'PUT', 'DELETE'] and pushover_settings is None:
            raise exceptions.NotFound(detail='does not exist for this user')

        if request.method == 'GET':
            serializer = serializers.PushoverSettingsSerializer(instance=pushover_settings)
            return Response(serializer.data)

        elif request.method == 'POST':
            if pushover_settings is not None:
                return Response({'detail': 'pushover-settings already exist for this user'},
                                status=status.HTTP_409_CONFLICT)
            pushover_settings = models.PushoverSettings(user=user)
            serializer = serializers.PushoverSettingsSerializer(instance=pushover_settings, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = serializers.PushoverSettingsSerializer(instance=pushover_settings, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        elif request.method == 'DELETE':
            pushover_settings.delete()
            return Response({'detail': 'successfully deleted'}, status=status.HTTP_204_NO_CONTENT)
