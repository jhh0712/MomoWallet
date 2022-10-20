import json
from datetime import date

from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from rest_framework import serializers, viewsets
from rest_framework.decorators import action

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def save(self, request):
        user = super().save()
        user.username = self.validated_data['username']
        user.email = self.validated_data['email']
        user.set_password(self.validated_data['password'])
        user.save()
        return user

    def validate(self, data):
        print('log : validate call')
        username = data.get('username', None)
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(f'username [{username}] already exists!')
        data['last_login'] = date.today()
        print('log : validate end')
        return data

class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['GET', 'POST'])
    def signup(self, request):
        print('log : signup call')
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save(request)
            token = RefreshToken.for_user(user)
            refresh = str(token)
            access = str(token.access_token)
            print(f'signup : {user}')
            return JsonResponse({'user': str(user),
                                 'access': access,
                                 'refresh': refresh}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'error': serializer.validate(request.data)},
                                status=status.HTTP_400_BAD_REQUEST)