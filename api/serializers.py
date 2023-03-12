from rest_framework import serializers
from databases.models import SurfaceUser

# class SurfaceUserSerializer(serializers.ModelSerializer):
#     name = serializers.CharField(max_length=50)
#     username = serializers.CharField(default='user',max_length=64)
#     password = serializers.CharField(default='',max_length=300)
#     is_active = serializers.BooleanField(default=False)
