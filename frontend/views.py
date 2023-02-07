from django.shortcuts import redirect, render
from django.http import HttpResponse
from .forms import AdminLoginForm
from django.contrib.auth import authenticate,login,logout
from databases.models import ClientAdmin
from scripts.admin_user.user_details import get_username_from_request
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
            username = request.POST.get("username")
            password = request.POST.get("password") 
            # authenticating the user and pass to get a user form user model
            user = authenticate(username=username,password=password)

            # checking if any such user is present in our User table
            if user is not None:
                login(request,user) #login the user to request's session
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
    return HttpResponse("ADMIN DASHBOAD HERE")

def logout_view(request):
    if str(request.user).lower() =="anonymoususer":
        return redirect('/auth/admin-login/')
    
    user = get_username_from_request(request)
    logout(request)
    msg_context= {
        'msg_color' : 'warning',
        'msg_title' : "See you soon," + user ,
        'msg_body' : "You have succesfully logged out!, don't forget to have your coffee, developer!",
        'msg_btn_link' : '/auth/admin-login/' ,
        'msg_btn_text' : 'Admin Login' 
            }
    return render(request,'main/messages.html',msg_context)