from django.urls import path
from .views import (
    ServerInitiateSuperuser,
)
urlpatterns = [
    path('server/initiate/superuser',ServerInitiateSuperuser.as_view())
]

