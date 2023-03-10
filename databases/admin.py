from django.contrib import admin

# Register your models here.
from .models import (
    LoginLog,
    ClientAdmin,
    Client,
    Quota,
    SurfaceUser,
    SurfaceUserAuthLog,
    ApiKeys,
    ClientVerificationToken,
    RequestLog,
    RechargeRate,
    PaymentsLog,
    LogApiRequests,
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
        'id',
    ]
admin.site.register(Quota,QuotaAdmin)



class SurfaceUserAdmin(admin.ModelAdmin):
    readonly_fields=[
        # 'id','timestamp'
    ]
admin.site.register(SurfaceUser,SurfaceUserAdmin)



class SurfaceUseAuthLogAdmin(admin.ModelAdmin):
    readonly_fields=[
        # 'id','timestamp'
    ]
admin.site.register(SurfaceUserAuthLog,SurfaceUseAuthLogAdmin)

class ApiKeysAdmin(admin.ModelAdmin):
    readonly_fields=[
        'id',
    ]
admin.site.register(ApiKeys,ApiKeysAdmin)


class ClientVerificationTokenAdmin(admin.ModelAdmin):
    readonly_fields = [
        
    ]
admin.site.register(ClientVerificationToken,ClientVerificationTokenAdmin)


class RequestLogAdmin(admin.ModelAdmin):
    readonly_fields = [
        'timestamp'
    ]
admin.site.register(RequestLog,RequestLogAdmin)


class RechargeRateAdmin(admin.ModelAdmin):
    readonly_fields = [
        'timestamp'
    ]
admin.site.register(RechargeRate,RechargeRateAdmin)

class PaymentsLogAdmin(admin.ModelAdmin):
    readonly_fields = [
        'timestamp'
    ]
admin.site.register(PaymentsLog,PaymentsLogAdmin)

class LogApiRequestsAdmin(admin.ModelAdmin):
    readonly_fields = [
        'timestamp'
    ]
admin.site.register(LogApiRequests,LogApiRequestsAdmin)

