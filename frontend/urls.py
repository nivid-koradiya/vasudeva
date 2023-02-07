from django.urls import path
from .views import admin_login,admin_dashbaord,logout_view
urlpatterns = [
    
    #dashboard urls
    path("dashboard/admin/",admin_dashbaord,name='admin_dashboard'),
    
    #authentication Urls
    path("auth/admin-login/",admin_login,name='admin_login'),
    path("auth/logout/",logout_view, name="logout"),
]
