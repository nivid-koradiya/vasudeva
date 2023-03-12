from databases.models import ( ClientAdmin,Client,Quota,RechargeRate,ApiKeys, ClientVerificationToken)
import time
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from scripts.admin_user.user_details import get_username_from_request, get_client_name_from_request
from scripts.logging.login_logout_logs import (
    admin_login_log,
    admin_logout_log,
    client_login_log,
    client_logout_log,
    )
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .forms import (AdminLoginForm,
                    AjaxNewClient,
                    AjaxNewClientAdmin,
                    AjaxClientSignup,
                    ClientLoginForm
                    )
from scripts.spark_mail import verification_mail as vfm
import environ
from scripts.network.ipadress import get_ip
from .decorators import log_ip_address
from scripts.payments import capture as  rz_capture
from scripts.payments import verify as  rz_verify
from django.views.decorators.csrf import csrf_exempt
from scripts.spark_mail import verification_mail 
from vasudeva.settings import ALLOWED_HOSTS
from datetime import datetime , timezone, timedelta
env = environ.Env()
environ.Env.read_env()

@log_ip_address
def admin_login(request):
    if request.user.is_authenticated:
        msg_context= {
                    'msg_color' : 'secondary',
                    'msg_title' : ("Welcome, "+ get_username_from_request(request)) ,
                    'msg_body' : "You are already loggedin, press the button below to access your dashbaord",
                    'msg_btn_link' : '/dashboard/admin/' ,
                    'msg_btn_text' : 'Procced to Dashbaord' 
                }
        return render(request,'main/messages.html',msg_context) # view message to already logged in user and ask tem to forward them selves
        # return redirect('/dashboard/admin') # forward the request to admin Dash if the client is already authenticated
    
    if request.method == "POST":
        # print("POST REQ")
        form = AdminLoginForm(request.POST)

        if form.is_valid(): # if form is valid the  move towards the authentication of recieved credentials
            # extracting the credentials from post request
            username = request.POST.get("username").lower()
            password = request.POST.get("password") 
            # authenticating the user and pass to get a user form user model
            user = authenticate(username=username,password=password)

            # checking if any such user is present in our User table
            if user is not None:
                if user.is_staff:
                    login(request,user) #login the user to  session
                    admin_login_log(request) # log the login record
                    
                else:
                    msg_context= {
                        'msg_color' : 'danger',
                        'msg_title' : "No Authorization!",
                        'msg_body' : "Seems that you have no authority to login in as admin!",
                        'msg_btn_link' : '' ,
                        'msg_btn_text' : 'Back to home' 
                    }
                    return render(request,'main/messages.html',msg_context,status=401)

                
                msg_context= {
                    'msg_color' : 'success',
                    'msg_title' : "Login success!",
                    'msg_body' : "You have successfully loggedin as admin, Make sure you manage data wisely!",
                    'msg_btn_link' : '/dashboard/admin' ,
                    'msg_btn_text' : 'Procced to Dashbaord' 
                }
                return render(request,'main/messages.html',msg_context)

            # if matching user is not found then we will push an error msg page
            else:
                msg_context= {
                    'msg_color' : 'danger',
                    'msg_title' : "Login Failed!",
                    'msg_body' : "You have entered the credentials for ADMIN wrong, make sure you are admin!",
                    'msg_btn_link' : '/auth/admin-login' ,
                    'msg_btn_text' : 'Retry Login' 
                }
                return render(request,'main/messages.html',msg_context,status=401)

        else:
            msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Enter a Valid Captcha!",
                    'msg_body' : "Try again with the form, make sure you fill the captcha right!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Try Again' 
                }
            return render(request,'main/messages.html',msg_context,status=401)

    #adding the form to the context that is being sent with the request to template
    context = dict()
    form = AdminLoginForm()
    context['form'] = form
    return render(request,'main/admin-login.html', context)

@log_ip_address
def admin_dashbaord(request):
    if str(request.user).lower() =="anonymoususer":
        return redirect('/auth/admin-login/')
    if request.user.is_staff:
        return render(request,'main/admin-dashboard.html')
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Not Authorized!",
                    'msg_body' : "You lack the permissions to access this portino of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/logout/' ,
                    'msg_btn_text' : 'Logout' 
                }
        return render(request,'main/messages.html',msg_context)
    
@log_ip_address
def logout_view(request):
    if str(request.user).lower() =="anonymoususer": #check if the non login user is trying to login.
        return redirect('/auth/admin-login/')
    

    user = get_username_from_request(request) # storing the username for messaging purpose.
    admin_logout_log(request) # log the logout record.
    logout(request)

    msg_context= {
        'msg_color' : 'warning',
        'msg_title' : "See you soon, " + user,
        'msg_body' : "You have succesfully logged out!, don't forget to have your coffee, developer!",
        'msg_btn_link' : '/auth/admin-login/',
        'msg_btn_text' : 'Admin Login',
    }
    return render(request,'main/messages.html',msg_context) # returning the logout message page.

@log_ip_address
def client_logout_view(request):
    if str(request.user).lower() =="anonymoususer": #check if the non login user is trying to login
        return redirect('/auth/client-login/')
    
    user = get_username_from_request(request) # storing the username for messaging purpose.
    client_logout_log(request) # log the logout record.
    logout(request)

    msg_context= {
        'msg_color' : 'warning',
        'msg_title' : "See you soon, " + user,
        'msg_body' : f"You have succesfully logged out!, have a good day!,{user}",
        'msg_btn_link' : '/auth/client-login/',
        'msg_btn_text' : 'Client Login',
    }
    return render(request,'main/messages.html',msg_context) # returning the logout message page.




#ADMIN  CLIENTS - ALL
@log_ip_address
def admin_all_client(request):
    if str(request.user).lower() =="anonymoususer":
        return redirect('/auth/admin-login/')
    if request.user.is_staff:
        clients =Client.objects.all()
        data = {
            'title' : 'Vasudeva Admin Dashboard',
            'clients' : clients
        }
        return render(request,'main/admin-client-all.html',data)
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Not Authorized!",
                    'msg_body' : "You lack the permissions to access this portion of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)



@log_ip_address
def admin_delete_client(request):
    if str(request.user).lower() =="anonymoususer":
        return redirect('/auth/admin-login/')
    if request.user.is_staff:
        clients =Client.objects.all()
        data = {
            'title' : 'Vasudeva Admin Dashboard',
            'clients' : clients
        }
        return render(request,'main/admin-client-delete.html',data)
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Not Authorized!",
                    'msg_body' : "You lack the permissions to access this portion of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)


@log_ip_address
def admin_client_admin_all(request):
    if str(request.user).lower() =="anonymoususer":
        return redirect('/auth/admin-login/')
    if request.user.is_staff:
        clients =ClientAdmin.objects.all()
        data = {
            'title' : 'Vasudeva Admin Dashboard',
            'clients' : clients
        }
        return render(request,'main/admin-clientadmin-all.html',data)
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Not Authorized!",
                    'msg_body' : "You lack the permissions to access this portion of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)

@log_ip_address
def admin_client_admin_manage(request):
    if str(request.user).lower() =="anonymoususer":
        return redirect('/auth/admin-login/')
    if request.user.is_staff:
        cl = Client.objects.all()
        clients =ClientAdmin.objects.all()
        data = {
            'title' : 'Vasudeva Admin Dashboard',
            'clients' : clients,
            'cl' : cl,
        }
        return render(request,'main/admin-clientadmin-manage.html',data)
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Not Authorized!",
                    'msg_body' : "You lack the permissions to access this portion of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)

@log_ip_address
def client_signup(request):
    if request.user.is_authenticated:
        msg_context= {
                    'msg_color' : 'secondary',
                    'msg_title' : ("Welcome, "+ get_username_from_request(request)) ,
                    'msg_body' : "You are already loggedin, press the button below to Recharge Account",
                    'msg_btn_link' : '/payment/recharge_portal' ,
                    'msg_btn_text' : 'Procced to Dashbaord' 
                }
        return render(request,'main/messages.html',msg_context)

    form = AjaxClientSignup()
    msg_context={
        'form' : form,
        # "qr" : str(request.headers['Cookie']).split('=')[-1],
    }
    return render(request,'main/client-signup.html',msg_context)


@log_ip_address
def client_login(request):
    if request.user.is_authenticated:
        msg_context= {
                    'msg_color' : 'secondary',
                    'msg_title' : ("Welcome, "+ get_username_from_request(request)) ,
                    'msg_body' : "You are already loggedin, press the button below to Recharge Account",
                    'msg_btn_link' : '/payment/recharge_portal' ,
                    'msg_btn_text' : 'Procced to Dashbaord' 
                }
        return render(request,'main/messages.html',msg_context)
    if request.method == "POST":
        # print("POST REQ")
        form = ClientLoginForm(request.POST)

        if form.is_valid(): # if form is valid the  move towards the authentication of recieved credentials
            # extracting the credentials from post request
            username = request.POST.get("username").lower()
            password = request.POST.get("password") 
            # authenticating the user and pass to get a user form user model
            user = authenticate(username=username,password=password)
            # checking if any such user is present in our User table
            if user is not None:
                if user is not None:
                    try:
                        user_client = ClientAdmin.objects.get(username=username)
                        client = user_client.client
                        if not client.is_active : 
                            msg_context= {
                                'msg_color' : 'warning',
                                'msg_title' : "Account INACTIVE",
                                'msg_body' : "Your API account has not been VERIFIED or Suspended by the vasudeva portal!",
                                'msg_btn_link' : '' ,
                                'msg_btn_text' : 'Back to Home' 
                            }
                            return render(request,'main/messages.html',msg_context,status=401)
                    except:
                        msg_context= {
                            'msg_color' : 'danger',
                            'msg_title' : "Login Authority is mismatched!",
                            'msg_body' : "You have entered the credentials for CLIENT mismatched with another staff user of VASUDEVA, make sure you are entering right password on this portal!",
                            'msg_btn_link' : '/auth/client-login' ,
                            'msg_btn_text' : 'Retry Login'
                        }
                        return render(request,'main/messages.html',msg_context)
                    
                    login(request,user) #login the user to  session
                    client_login_log(request) # log the login record
                    # print(user)
                else:
                    msg_context= {
                        'msg_color' : 'danger',
                        'msg_title' : "No Authorization!",
                        'msg_body' : "Seems that you have no authority to login in as Client!",
                        'msg_btn_link' : '/' ,
                        'msg_btn_text' : 'Back to home' ,

                        
                    }
                    return render(request,'main/messages.html',msg_context,status=401)

                
                msg_context= {
                    'msg_color' : 'success',
                    'msg_title' : "Login success!",
                    'msg_body' : "You have successfully loggedin as Client, Make sure you Pay for your requirements wisely!",
                    'msg_btn_link' : '/payment/recharge_portal' ,
                    'msg_btn_text' : 'Procced to Dashbaord' 
                }
                return render(request,'main/messages.html',msg_context)

            # if matching user is not found then we will push an error msg page
            else:
                msg_context= {
                    'msg_color' : 'danger',
                    'msg_title' : "Login Failed!",
                    'msg_body' : "You have entered the credentials for Client wrong, make sure you are entering correct credentials!",
                    'msg_btn_link' : '/auth/client-login' ,
                    'msg_btn_text' : 'Retry Login' 
                }
                return render(request,'main/messages.html',msg_context,status=401)

        else:
            msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Enter a Valid Captcha!",
                    'msg_body' : "Try again with the form, make sure you fill the captcha right!",
                    'msg_btn_link' : '/auth/client-login/' ,
                    'msg_btn_text' : 'Try Again' 
                }
            return render(request,'main/messages.html',msg_context,status=401)

    context={}
    form = ClientLoginForm()
    context['form'] = form
    return render(request=request,template_name='main/client-login.html',context=context)


@log_ip_address
def index_view(request):
    return render(request=request,template_name='main/index.html')

@log_ip_address
def recharge_portal(request):
    if request.user.is_authenticated:
        context ={}
        rate_list = RechargeRate.objects.order_by("-timestamp")[0]
        context['mail_rate'] = rate_list.mail_rate
        context['request_rate'] = rate_list.request_rate
        return render(request,"main/recharge_portal.html",context)
    else: 
        msg_context= {
                    'msg_color' : 'danger',
                    'msg_title' : "Login Required!",
                    'msg_body' : "To recharge your account you need to login first!",
                    'msg_btn_link' : '/auth/client-login' ,
                    'msg_btn_text' : 'Login' 
                }
        return render(request,'main/messages.html',msg_context,status=401)
@log_ip_address
def payment_portal(request):
    if request.method == 'POST':
        username = request.user.username
        client_admin = ClientAdmin.objects.filter(username = username)
        if len(client_admin) == 1:
            context = {}
            try:
                amount = int(request.POST.get('amount'))
            except:
                msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Amount Error!",
                    'msg_body' : "Try it with integral values only for better recharge benifits!",
                    'msg_btn_link' : '/payment/recharge_portal/' ,
                    'msg_btn_text' : 'Recharge Portal' 
                }
                return render(request,'main/messages.html',msg_context)
            context = rz_capture.gen_order(amount)
            rate_list = RechargeRate.objects.order_by("-timestamp")[0]
            context['mail_rate'] = rate_list.mail_rate
            context['request_rate'] = rate_list.request_rate
            context['user_amount'] = amount
            client = client_admin[0].client
            context['contact'] = client.mobile
            context['name'] = client.organisation
            context['email'] = client_admin[0].email
            print(context)
            return render(request,"main/payment_portal.html",context)
        else: 
            msg_context= {
                    'msg_color' : 'danger',
                    'msg_title' : "Authorisation Elevation required!",
                    'msg_body' : "Try again with different user !",
                    'msg_btn_link' : '/auth/client-login/' ,
                    'msg_btn_text' : 'Client Login' 
                }
            return render(request,'main/messages.html',msg_context)
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Server Purpose page only!",
                    'msg_body' : "Cannot navigate the page as a human!",
                    'msg_btn_link' : '/payment/recharge_portal/' ,
                    'msg_btn_text' : 'Back to Reharge Portal' 
                }
        return render(request,'main/messages.html',msg_context)

@csrf_exempt
@log_ip_address
def payment_handler(request):
    print(request.POST)
    if request.method == 'POST':
        try:
            rz_verify.verify_payment(request)
            msg_context= {
                    'msg_color' : 'success',
                    'msg_title' : "Your Payment is Successful",
                    'msg_body' : "Your payment has been recieved successfully by Vasudeva!",
                    'msg_btn_link' : '/payment/recharge_portal/' ,
                    'msg_btn_text' : 'Back to recharge Portal' ,
                    'msg_btn2_link' : '/auth/logout/' ,
                    'msg_btn2_text' : 'Logout' ,
                }
            return render(request,'main/messages.html',msg_context)
            
        except:
            msg_context= {
                    'msg_color' : 'danger',
                    'msg_title' : "Your Payment Failed !",
                    'msg_body' : "Your payment has been failed ue to technical issues!",
                    'msg_btn_link' : '/payment/recharge_portal/' ,
                    'msg_btn_text' : 'Back to recharge Portal' 
                }
            return render(request,'main/messages.html',msg_context)
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Server Purpose page only!",
                    'msg_body' : "Cannot navigate the page as a human!",
                    'msg_btn_link' : '/payment/recharge_portal/' ,
                    'msg_btn_text' : 'Back to Reharge Portal' 
                }
        return render(request,'main/messages.html',msg_context)

def admin_apikey_all(request):
    if str(request.user).lower() =="anonymoususer":
        return redirect('/auth/admin-login/')
    if request.user.is_staff:
        keys = ApiKeys.objects.all().order_by('client')
        ca = ClientAdmin.objects.all().order_by('client')
        print(keys)
        print(ca)
        keys = zip(keys,ca)
        data = {
            'title' : 'Vasudeva Admin Dashboard',
            "keys": keys
        }
        return render(request,'main/admin-apikey-all.html',data)
    else:
        msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Not Authorized!",
                    'msg_body' : "You lack the permissions to access this portion of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)
    


def verify_client(request):
    token = str(request.GET.get('token'))
    print(token)
    try : 
        verif_token = ClientVerificationToken.objects.get(token=token)
        delta = verif_token.timestamp - datetime.now(timezone.utc)
        if delta.seconds <= 86400 :
            client = verif_token.client
            if client.is_active == True:
                msg_context= {
                        'msg_color' : 'secondary',
                        'msg_title' : f"{str(verif_token.client).upper()} ALREADY VERIFIED !",
                        'msg_body'  :  "Your organisation is already verified from our side, please login to access the portal!",
                        'msg_btn_link' : '/auth/client-login/' ,
                        'msg_btn_text' : 'Login' 
                    }
            
                return render(request,'main/messages.html',msg_context)
            
            client.is_active = True
            client.save()
            msg_context= {
                        'msg_color' : 'success',
                        'msg_title' : f"{str(verif_token.client).upper()} Verified !",
                        'msg_body'  :  "Your organisation is verified successfully, you will soon recieve the API credentials on the mail, until you may visit out recharge facility after logging in!",
                        'msg_btn_link' : '/auth/client-login/' ,
                        'msg_btn_text' : 'Login' 
                    }
            
            return render(request,'main/messages.html',msg_context)
            
        else:
            msg_context= {
                        'msg_color' : 'warning',
                        'msg_title' : f"Token-Expired !",
                        'msg_body'  :  f"Your token was Expired on {verif_token.timestamp + timedelta(0,86400)}",
                        'msg_btn_link' : '/auth/client-login/' ,
                        'msg_btn_text' : 'Back to Login' 
                    }
            return render(request,'main/messages.html',msg_context)
    except:
        msg_context= {
                        'msg_color' : 'danger',
                        'msg_title' : "Verification token not found !",
                        'msg_body'  :  "Token you are trying to verify is not a valid token, in-case of any inconvienience contact - devflix.mail.me@gmail.com !",
                        'msg_btn_link' : '/' ,
                        'msg_btn_text' : 'Back to Home' 
                    }
        return render(request,'main/messages.html',msg_context)








# AJAX REQUESTS HANDLING VIEWS:

def ajax_client_delete(request):
    status = None
    deleted_id = None
    try:
        id = request.POST.get('client_id')
        # fetching the client entities
        client = Client.objects.get(id = id)
        api_key = ApiKeys.objects.get(client = client)
        client_admin = ClientAdmin.objects.get(client=client)
        quota = Quota.objects.get(client=client)
        client.delete()
        api_key.delete()
        client_admin.delete()
        quota.delete()
        # print(client)
        # print(api_key)
        # print(quota.quantity)
        # print(client_admin.email)
        #returning the deleted item id and the status as True
        return  JsonResponse({
            'deleted' : True,
            'id' : id
        })
        
    except:
        return  JsonResponse({
            'deleted' : False,
            'id' : None
        })

def ajax_client_status(request):
    status = None
    deleted_id = None
    try:
        id = request.POST.get('client_id')
        client = Client.objects.get(id = id)
        client.is_active = not (client.is_active)
        client.save()
        return  JsonResponse({
            'success' : True
        })

    except:
        return  JsonResponse({
            'success' : False
        })




def ajax_client_new(request):
    status = None
    deleted_id = None
    try:
        # print(request.POST)
        form = AjaxNewClient(request.POST)
        if form.is_valid():
            client = Client()
            client.organisation = request.POST.get('company')
            client.mobile = request.POST.get('phone')
            client.save()
            api_key = ApiKeys()
            api_key.client = client
            api_key.save()
            org_quota = Quota()
            org_quota.quantity =100
            org_quota.client = client
            org_quota.mail = 10
            org_quota.save()
            
            return  JsonResponse({
                'success' : True
            })
            
        else:
            return  JsonResponse({
                'success' : False
            })
    except:
        return  JsonResponse({
            'success' : False
        })
        
        
#CLIENTADMINS AJAX REQUEST HANDLERS

def ajax_clientadmin_status(request):
    status = None
    deleted_id = None
    try:
        id = request.POST.get('client_id')
        client = ClientAdmin.objects.get(id = id)
        client.is_active = not (client.is_active)
        client.save()
        return  JsonResponse({
            'success' : True
        })
        
    except:
        return  JsonResponse({
            'success' : False
        })
        
def ajax_clientadmin_new(request):
    status = None
    deleted_id = None
    try:
        # print(request.POST)
        form = AjaxNewClientAdmin(request.POST)
        if form.is_valid():
            # print("FORRRRRRMMMM VALID!!!!")
            client_admin = ClientAdmin()
            client_admin.username = request.POST.get('username')
            client_admin.name = request.POST.get('name')
            client_admin.email = request.POST.get('email')
            client_admin.client = Client.objects.get(id = request.POST.get('user_select'))
            user = User()
            user.username =request.POST.get('username')
            user.set_password(request.POST.get('password'))
            user.is_active = True
            user.save()
            client_admin.user = user
            client_admin.save()            
            return  JsonResponse({
                'success' : True
            })
        else:
            return  JsonResponse({
                'success' : False
            })
    except:
        return  JsonResponse({
            'success' : False
        })

def ajax_new_client_signup(request):
    if request.method == "POST":
        print(request.POST)
        rec_form = AjaxClientSignup(request.POST)
        if rec_form.is_valid():
            try:
                client = Client()
                client.organisation = request.POST.get('org_name')
                client.mobile = request.POST.get('mobile')
                client.save()
                org_quota = Quota()
                org_quota.quantity =100
                org_quota.client = client
                org_quota.mail = 10
                org_quota.save()
                client_admin = ClientAdmin()
                client_admin.username = request.POST.get('username')
                client_admin.name = request.POST.get('name')
                client_admin.email = request.POST.get('email')
                client_admin.client = client
                user = User()
                user.username =request.POST.get('username')
                user.set_password(request.POST.get('password'))
                user.is_active = True
                user.save()
                client_admin.user = user
                client_admin.save()    
                api_key = ApiKeys()
                api_key.client = client
                api_key.save()
                verif_tok = ClientVerificationToken()
                verif_tok.client = client
                verif_tok.save()
                verf_url = "http://"+ env('HOST')+ '/verify/client/?token=' + str(verif_tok.token)
                data={'id' : client.id,'url': verf_url}
                verification_mail.send_email(subject="Verification Mail for Accessing Account!",recipients=str(client_admin.email),data=data)
                time.sleep(2)
                return JsonResponse({
                'status' : True,
                })
            except:
                return JsonResponse({
                'status' : False,
                })
            
        else:
            errors = (rec_form.errors)
            print(errors)
            time.sleep(5)
            return JsonResponse({
            'status' : False,
            'error' : errors
            })

    else:
        time.sleep(5)
        return JsonResponse({
        'status' : False,
    })
    




#test views 

def test_view_1(request):
    
    # subject = "Email Subject"
    # recipients = ['nividkoradiya@gmail.com']
    # data = {
    #     'id' : request.GET.get('id'),
    #     'url' : request.GET.get('url'),
    # }
    # vfm.send_email(subject, recipients,data)
    # return HttpResponse("SENT")
    # ClientAdmin.objects.all().delete()
    # Client.objects.all().delete()
    # ApiKeys.objects.all().delete()
    # Quota.objects.all().delete()
    # ClientVerificationToken.objects.all().delete()
    return HttpResponse("ALL CLIENT'S DATA FLUSHED FROM DATABASE")
