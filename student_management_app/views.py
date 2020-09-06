import json

import requests
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

# @csrf_exempt
def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        captcha_token=request.POST.get("g-recaptcha-response")
        cap_url = "https://www.google.com/recaptcha/api/siteverify"
        cap_secret = "*********************************"
        cap_data={"secret":cap_secret,"response":captcha_token}
        cap_server_response = requests.post(url=cap_url,data=cap_data)
        cap_json = json.loads(cap_server_response.text)
        if cap_json['success']==False:
            messages.error(request, "Invalid Captcha Try Again")
            return HttpResponseRedirect("/")
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

def showFirebaseJS(request):
    data = ['importScripts("https://www.gstatic.com/firebasejs/7.19.1/firebase-app.js");' \



           'importScripts("https://www.gstatic.com/firebasejs/7.19.1/firebase-messaging.js");' \

           'var firebaseConfig = {' \
           '             apiKey: "AIzaSyD2s0wpsQkvNVCAsPohTSRQPU4oH8DgTho",' \
           '         authDomain: "studentmanagementsystem-d8ec6.firebaseapp.com",' \
           '         databaseURL: "https://studentmanagementsystem-d8ec6.firebaseio.com",' \
           '         projectId: "studentmanagementsystem-d8ec6",' \
           '         storageBucket: "studentmanagementsystem-d8ec6.appspot.com",' \
           '         messagingSenderId: "861557177929",' \
           '         appId: "1:861557177929:web:d568ea1be0c3fc79dc8998",' \
           '         measurementId: "G-8812Z7EQH7"' \
           '     };' \

           'firebase.initializeApp(firebaseConfig);' \
           'const messaging-firebase.messaging();' \

           'messaging.setBackgroundMessagingHandler(function (payload) {' \
           '    console.log(payload)' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon,' \
           '    }' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);'  \
           '});']

    return HttpResponse(data,content_type="text/javascript")

def Testurl(request):
    return HttpResponse("OK")