from databases.models import ClientAdmin,Client
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect, render
from scripts.admin_user.user_details import get_username_from_request
from scripts.logging.login_logout_logs import admin_login_log, admin_logout_log
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .forms import (AdminLoginForm,AjaxNewClient,AjaxNewClientAdmin
                    )


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
                    return render(request,'main/messages.html',msg_context)

                
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
                return render(request,'main/messages.html',msg_context)

        else:
            msg_context= {
                    'msg_color' : 'warning',
                    'msg_title' : "Enter a Valid Captcha!",
                    'msg_body' : "Try again with the form, make sure you fill the captcha right!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Try Again' 
                }
            return render(request,'main/messages.html',msg_context)

    #adding the form to the context that is being sent with the request to template
    context = dict()
    form = AdminLoginForm()
    context['form'] = form
    return render(request,'main/admin-login.html', context)

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
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)

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




#ADMIN  CLIENTS - ALL
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
                    'msg_body' : "You lack the permissions to access this portino of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)




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
                    'msg_body' : "You lack the permissions to access this portino of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)



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
                    'msg_body' : "You lack the permissions to access this portino of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)


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
                    'msg_body' : "You lack the permissions to access this portino of admin sections, Try logging in as ad Admin!",
                    'msg_btn_link' : '/auth/admin-login/' ,
                    'msg_btn_text' : 'Admin Login' 
                }
        return render(request,'main/messages.html',msg_context)



def client_signup(request):
    msg_context={
        
    }
    return render(request,'main/client-signup.html',msg_context)


# AJAX REQUESTS HANDLING VIEWS:

def ajax_client_delete(request):
    status = None
    deleted_id = None
    try:
        id = request.POST.get('client_id')
        # Client.objects.get(id = id).delete()
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