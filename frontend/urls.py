from django.urls import path
from .views import (
    admin_login,admin_dashbaord,
    logout_view,
    admin_all_client,
    admin_delete_client,
    admin_client_admin_all,
    admin_client_admin_manage,
    client_signup,
    client_login,
    
    #ajax requests.
    ajax_client_delete,
    ajax_client_status,
    ajax_client_new,
    ajax_clientadmin_status,
    ajax_clientadmin_new,
    ajax_new_client_signup,
    
    
    #test_views
    test_view_1,
    
    #index views
    index_view,

    )
urlpatterns = [
    #index page
    path('',index_view,name='index_view'),
    #dashboard urls
    path("dashboard/admin/",admin_dashbaord,name='admin_dashboard'),
    path("dashboard/admin/client/all",admin_all_client,name='client_all'),
    # path("dashboard/admin/client/add",admin_add_client,name='client_add'),
    path("dashboard/admin/client/manage",admin_delete_client,name='client_manage'),
    path("dashboard/admin/clientadmin/all",admin_client_admin_all,name='clientadmin_all'),
    path("dashboard/admin/clientadmin/manage",admin_client_admin_manage,name='clientadmin_manage'),
    # /dashboard/admin/clientadmin/all
    
    #AJAX REQUESTS
    path("data/client/delete",ajax_client_delete,name='ajax_client_delete'),
    path("data/client/status",ajax_client_status,name='ajax_client_status'),
    path("data/client/new",ajax_client_new,name='ajax_client_new'),
    path("data/clientadmin/status",ajax_clientadmin_status,name='ajax_clientadmin_status'),
    path("data/clientadmin/new",ajax_clientadmin_new,name='ajax_clientadmin_new'),
    path("data/client/signup",ajax_new_client_signup,name='ajax_new_client_signup'),
    #authentication Urls
    path("auth/admin-login/",admin_login,name='admin_login'),
    path("auth/client-signup/",client_signup,name='client_signup'),
    path("auth/client-login/",client_login,name='client_login'),
    path("auth/logout/",logout_view, name="logout"),
    
    
    #test_views
    path("test/1/",test_view_1, name="test_view_1"),
    

    
]
