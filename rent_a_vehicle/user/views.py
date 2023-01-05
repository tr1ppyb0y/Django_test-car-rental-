from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from user import serializers as user_serializer

from .models import User, UserLoginLogs

# Create your views here.


@csrf_exempt
@api_view(['POST'])
def sign_me_up(request):
    serializer = user_serializer.SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        token = Token.objects.create(user=user)
        UserLoginLogs.objects.create(user=user, user_type=user.user_type)
        return JsonResponse({'message':'sign-up successfull', 'token':token.key})
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def log_me_in(request):
    serializer = user_serializer.LoginSerializer(data=request.query_params)
    if serializer.is_valid(raise_exception=True):
        creds = serializer.validated_data
        creds_dict = dict(creds.items())
        try:
            user = User.objects.get(username=creds_dict['username'])
        except User.DoesNotExist as err:
            content = {
                'status': 'Error',
                'message': str(err)
            }
            return JsonResponse(content, status=400)
        if user.check_password(creds_dict['password']):
            token = Token.objects.create(user=user)
            UserLoginLogs.objects.create(user=user, user_type=user.user_type)
            return JsonResponse({'message':'login successfull', 'token':token.key})
        else:
            return JsonResponse({'message': 'Invalid ID or password'})
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@authentication_classes([TokenAuthentication, ])
@permission_classes([permissions.IsAuthenticated, ])
@api_view(['GET'])
def log_me_out(request):
    Token.objects.get(user=request.user).delete()
    return JsonResponse({'message': 'logged out successfully.'})


class ListUserLogsView(generics.ListAPIView):
    queryset = UserLoginLogs.objects.all()
    authentication_classes = (TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )
    serializer_class = user_serializer.LoginLogsSerializers

    def get(self, request, *args, **kwargs):
        if self.request.user.user_type == 'admin':
            return super().get(request, *args, **kwargs)
        else:
            return UserLoginLogs.objects.none()
