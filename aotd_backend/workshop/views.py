from rest_framework import viewsets, mixins, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
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


# TODO: API endpoints for user-settings
class UserSettingsViewSet(
    viewsets.GenericViewSet,
):
    permission_classes = [IsAuthenticated]
    queryset = models.UserSettings.objects.all()
    serializer_class = serializers.UserSettingsSerializer

    @action(detail=False, methods=['GET', 'POST', 'PUT'])  # endpoint: 'user-settings/me'
    def me(self, request):
        user: models.CustomUser = request.user
        user_settings, created = models.UserSettings.objects.get_or_create(user=user)

        if request.method == 'GET':
            serializer = serializers.UserSettingsSerializer(user_settings)
            return Response(serializer.data)

        elif request.method == 'POST':
            if created:
                serializer = serializers.UserSettingsSerializer(user_settings, data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
            else:
                return Response({'detail': 'user-settings already exist for this user'},
                                status=status.HTTP_409_CONFLICT)

        elif request.method == 'PUT':
            serializer = serializers.UserSettingsSerializer(user_settings, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

# TODO: API endpoints for pushover-settings
