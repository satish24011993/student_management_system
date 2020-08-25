from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from student_management_app.EmailBackEnd import EmailBackEnd
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def showDemoPage(request):
    return render(request,"demo.html")

def ShowLoginPage(request):
    return render(request, "login_page.html")

@csrf_exempt
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        user = EmailBackEnd.authenticate(request,username = request.POST.get("email"),password = request.POST.get("password"))
        if user != None:
            login(request,user)  
            if user.user_type=="1":
                return HttpResponseRedirect('admin_home/')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse('staff_home'))
            else:
                return HttpResponseRedirect(reverse('student_home'))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+" usertype : "+request.user.user_type)
    else:
        return HttpResponse("Please Give Login Credintials")

def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")