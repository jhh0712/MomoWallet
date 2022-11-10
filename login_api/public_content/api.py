from django.http import JsonResponse
from rest_framework import serializers, viewsets
from rest_framework import status
from rest_framework.decorators import action

from public_content.models import Version


class VersionSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

    def save(self, request):
        version = super().save()
        version.app_version = self.validated_data['app_version']
        version.save()
        return version


class VersionSaveViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSaveSerializer

    @action(detail=False, methods=['POST'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            version = serializer.save(request)
            return JsonResponse({'version': version.app_version}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'version save fail'},
                                status=status.HTTP_400_BAD_REQUEST)


class VersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Version
        fields = '__all__'

    def validate(self, data):
        app_version = data.get('app_version')
        if Version.objects.filter(app_version=app_version).exists():
            latest_version = Version.objects.latest('app_version')
            print(f'{latest_version.app_version} {app_version}')
            if app_version == latest_version.app_version:
                return {'content': 'Current App is Latest'}
            elif app_version < latest_version.app_version:
                return {'content': 'New Version Exist! Update App!'}
            else:
                return {'error': 'Version Invaild'}
        else:
            return {'error': 'Version Not Exist'}


class VersionViewSet(viewsets.ModelViewSet):
    queryset = Version.objects.all()
    serializer_class = VersionSerializer

    @action(detail=False, methods=['POST'])
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            return JsonResponse(serializer.validate(request.data), status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'{e}'},
                                status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['POST'])
    def save(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            version = serializer.save(request)
            return JsonResponse({'version': version}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': 'version save fail'},
                                status=status.HTTP_400_BAD_REQUEST)
