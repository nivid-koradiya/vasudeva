from django.urls import path
from .views import (
    admin_login,admin_dashbaord,
    logout_view,
    admin_all_client,
    # admin_add_client,
    admin_delete_client,
    )
urlpatterns = [
    
    #dashboard urls
    path("dashboard/admin/",admin_dashbaord,name='admin_dashboard'),
    path("dashboard/admin/client/all",admin_all_client,name='client_all'),
    # path("dashboard/admin/client/add",admin_add_client,name='client_add'),
    path("dashboard/admin/client/delete",admin_delete_client,name='client_delete'),
    
    #authentication Urls
    path("auth/admin-login/",admin_login,name='admin_login'),
    path("auth/logout/",logout_view, name="logout"),
]
