from django.urls import path
from .views import (
    ServerInitiateSuperuser,
    TestingEndpoint,
    CreateSurfaceUser,
    GetSurfaceUser,
    AuthenticateSurfaceUser,
    
)
urlpatterns = [
    path('server/initiate/superuser',ServerInitiateSuperuser.as_view(),name="superuser_initiate"),
    #testing endpoints
    path("test/",TestingEndpoint.as_view(), name="testing_endpoint"),
    path("users/create/",CreateSurfaceUser.as_view(), name="create_user"),
    path("users/get/",GetSurfaceUser.as_view(), name="get_user"),
    path("users/authenticate/",AuthenticateSurfaceUser.as_view(), name="create_user"),
]
