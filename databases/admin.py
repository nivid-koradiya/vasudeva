from django.contrib import admin

# Register your models here.
from .models import (
    LoginLog,
    ClientAdmin,
    Client,
    Quota
)

class LoginLogAdmin(admin.ModelAdmin):
    readonly_fields=[
        # 'id','timestamp'
    ]
admin.site.register(LoginLog,LoginLogAdmin)

class ClientAdminAdmin(admin.ModelAdmin):
    readonly_fields=[
        # 'id','timestamp'
    ]
admin.site.register(ClientAdmin,ClientAdminAdmin)


class ClientAdmin(admin.ModelAdmin):
    readonly_fields=[
        # 'id','timestamp'
    ]
admin.site.register(Client,ClientAdmin)



class QuotaAdmin(admin.ModelAdmin):
    readonly_fields=[
        # 'id','timestamp'
    ]
admin.site.register(Quota,QuotaAdmin)