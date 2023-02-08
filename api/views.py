from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from scripts.server.initiation.superuser import initiate_superuser


class ServerInitiateSuperuser(APIView):
    def post(self, request, *args, **kwargs):
        auth = request.headers.get('Authorization')
        if initiate_superuser(auth):
            response = Response(data = {
                'status' : True,
                'message': 'Super user created successfully'
                },status=200)
            return response
        else:
            return Response(data ={
                "status" : False,
                'message' : "User already exist or the database server is not responding!"
            }, status=409)


def server_initiate_superuser(request):
    
    return HttpResponse('REQUEST ACCEPTED')

