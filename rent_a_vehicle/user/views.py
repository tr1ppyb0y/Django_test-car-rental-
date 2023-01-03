from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from user import serializers as user_serializer
from django.http import JsonResponse
from .models import User, UserLoginLogs

# Create your views here.


@csrf_exempt
@api_view(['POST'])
def sign_up(request):
    serializer = user_serializer.SignUpSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET'])
def login(request):
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
            # Implementation pending.
            # login(request, user)
            UserLoginLogs(user=user, user_type=user.user_type)
            return JsonResponse({'message':'login successfull'})
        else:
            return JsonResponse({'message': 'Invalid ID or password'})
    return JsonResponse(serializer.errors, status=400)
