from django.urls import path
from .views import (
    admin_login,admin_dashbaord,
    logout_view,
    admin_all_client,
    # admin_add_client,
    admin_delete_client,
    
    #ajax requests.
    ajax_client_delete,
    ajax_client_status,
    ajax_client_new
    

    )
urlpatterns = [
    
    #dashboard urls
    path("dashboard/admin/",admin_dashbaord,name='admin_dashboard'),
    path("dashboard/admin/client/all",admin_all_client,name='client_all'),
    # path("dashboard/admin/client/add",admin_add_client,name='client_add'),
    path("dashboard/admin/client/manage",admin_delete_client,name='client_manage'),
    
    #AJAX REQUESTS
    path("data/client/delete",ajax_client_delete,name='ajax_client_delete'),
    path("data/client/status",ajax_client_status,name='ajax_client_status'),
    path("data/client/new",ajax_client_new,name='ajax_client_new'),
    
    #authentication Urls
    path("auth/admin-login/",admin_login,name='admin_login'),
    path("auth/logout/",logout_view, name="logout"),
    

    
]
