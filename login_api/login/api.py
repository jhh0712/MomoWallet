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


class UserRegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    @action(detail=False, methods=['GET', 'POST'])
    def post(self, request):
        print('log : signup call2')
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


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        print('log : validate call')
        username = data.get('username')
        password = data.get('password', None)
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)

            if not user.check_password(password):
                raise serializers.ValidationError('Wrong Password!')
                return {'error': 'wrong password'}
        else:
            raise serializers.ValidationError('Not Exist User!')
            return {'error': 'not exist user'}

        token = RefreshToken.for_user(user)
        refresh = str(token)
        access = str(token.access_token)

        return {'username': username, 'refresh': refresh, 'access': access}


class UserAuthViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthSerializer

    @action(detail=False, methods=['GET', 'POST'])
    def post(self, request):
        print('log : signin call')
        serializer = self.serializer_class(data=request.data)
        try:
            return JsonResponse(serializer.validate(request.data), status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({'error': f'{e}'},
                                status=status.HTTP_400_BAD_REQUEST)



