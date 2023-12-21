from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth.hashers import make_password,check_password
from .models import User
from django.core.cache import cache
import jwt

#memurai serveer = 6379

header = {  
  "alg": "HS256",  
  "typ": "JWT"  
}   
secret = "raghuram"

@api_view(['GET'])
def api_home(request):
    return Response({"message":"home page"})

@api_view(['GET'])
def users(request):
    users = User.objects.all()
    serializer = UserSerializer(users,many=True)
    return Response(serializer.data)


@api_view(['POST'])
def register(request):
    users = User.objects.all()
    for user in users:
        if user.username == request.data['username']:
            return HttpResponse("Username already exists")
    request.data['password'] = make_password(request.data['password'])
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    token = jwt.encode(
        {'username':serializer.data['username'],
         'userId':serializer.data['id']},
         secret,algorithm='HS256',headers=header)
    print(token)
    response = {    
        "username":serializer.data['username'],
        "id":serializer.data['id'],
        "token":token
    }
    cache.set(token,"ok",timeout=300)
    return Response(response)

@api_view(['POST'])
def login(request):
    requestUsername = request.data['username']
    requestPassword = request.data['password']
    user = User.objects.filter(username=requestUsername).values()
    if len(user)==0:
        return HttpResponse("User does not exist")
    print(user[0]['password'])
    authenticated = check_password(requestPassword,user[0]['password'])
    if authenticated:
        serializer = UserSerializer(data=user,many=True)
        serializer.is_valid()
        token = jwt.encode(
        {'username':serializer.data[0]['username'],
         'userId':serializer.data[0]['id']},
         secret,algorithm='HS256',headers=header)
        print(token)
        response = {    
            "username":serializer.data[0]['username'],
            "id":serializer.data[0]['id'],
            "token":token
        }
        cache.set(token,"ok",timeout=300)
        return Response(response)
    else:
        return HttpResponse("Unauthorised")
    # return HttpResponse("ok") 

@api_view(['POST'])
def get_cache(request):
    if cache.get(request.data['token']):
        token = request.data['token']
        decoded = jwt.decode(token,secret,algorithms='HS256')
        return Response(decoded)
    else:
        return Response({"message":"no cache"})
    
@api_view(['POST'])
def delete_cache(request):
    if cache.get(request.data['token']):
        cache.delete(request.data['token'])
        return Response({"message":"deleted"})
    
@api_view(['GET'])
def clear_cache(request):
    cache.clear()
    return Response({"message":"cache cleared"})