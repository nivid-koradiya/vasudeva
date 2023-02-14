from django.urls import path
from .views import (
    ServerInitiateSuperuser,
    TestingEndpoint
)
urlpatterns = [
    path('server/initiate/superuser',ServerInitiateSuperuser.as_view(),name="superuser_initiate"),
    #testing endpoints
    path("test/",TestingEndpoint.as_view(), name="testing_endpoint"),
]

