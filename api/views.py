from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from scripts.server.initiation.superuser import initiate_superuser
from rest_framework import permissions
from scripts.api_scripts import quotas,client,surfaceusers
from .permissions import (
    ApiKeyPermission
)

class ServerInitiateSuperuser(APIView):
    def post(self, request, *args, **kwargs):
        auth = request.headers.get('Authorization')
        if initiate_superuser(auth):
            response = Response(data = {
                'status' : True,
                'message': 'Super user created statusfully'
                },status=200)
            return response
        else:
            return Response(data ={
                "status" : False,
                'message' : "User already exist or the database server is not responding!"
            }, status=409)


def server_initiate_superuser(request):
    return HttpResponse('REQUEST ACCEPTED')


class TestingEndpoint(APIView):
    permission_classes = [ApiKeyPermission]
    def post(self,request,*args, **kwargs):
        if quotas.deduct_quota_request(request):            
            return Response(data={
                
                'status': True
            })
        else:
            return Response(data={
                "status" : False,
                'error' : "Quota Limits reached!"
            },status=403)
            
class CreateSurfaceUser(APIView):
    permission_classes = [ApiKeyPermission]
    def post(self,request,*args, **kwargs):
        if quotas.deduct_quota_request(request): 
            try: 
                user = surfaceusers.create_surfaceuser(request)
                if user:    
                    return Response(data={
                    'status': True,
                    'user' : user
                    })
                else:
                    return Response(data={
                    'status': False,
                    'message' : 'User with similar details already exist!',
                    },status=409)
            except:
                
                return Response(data={
                'status': False
                },status=500)
        else:
            return Response(data={
                "status" : False,
                'error' : "Quota Limits reached!"
            },status=403)

class GetSurfaceUser(APIView):
    permission_classes = [ApiKeyPermission]
    def get(self,request,*args, **kwargs):
        if quotas.deduct_quota_request(request): 
            try: 
                user = surfaceusers.get_surfaceuser(request)
                if user:    
                    return Response(data={
                    'status': True,
                    'user' : user
                    })
                else:
                    return Response(data={
                    'status': False,
                    'message' : "User with similar details don't exist!",
                    },status=404)
            except:
                
                return Response(data={
                'status': False
                },status=500)
        else:
            return Response(data={
                "status" : False,
                'error' : "Quota Limits reached!"
            },status=403)

class AuthenticateSurfaceUser(APIView):
    permission_classes = [ApiKeyPermission]
    def post(self,request,*args, **kwargs):
        if quotas.deduct_quota_request(request): 
            try: 
                atuh_status = surfaceusers.authenticate_surfaceuser(request)
                if atuh_status:    
                    return Response(data={
                    'status': atuh_status
                    })
                else:
                    return Response(data={
                    'status': {'authenticated' : False},

                    'message' : "User cant be authenticated!",
                    },status=404)
            except:
                
                return Response(data={
                'status': False
                },status=500)
        else:
            return Response(data={
                "status" : False,
                'error' : "Quota Limits reached!"
            },status=403)

