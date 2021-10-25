from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import string
from .models import shorturl
from django.core.mail import send_mail
from django.conf import settings
import re
# Create your views here.


def randomshort():
    return ''.join(random.choices(string.ascii_letters,k=7))

def passwordcheck(v):
    if(len(v)>=8):
        if(bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})',v))==True):
            return 10
        elif(bool(re.match('((\d*)([a-z]*)([A-Z]*)([!@#$%^&*]*).{8,30})',v))==True):
            return -2
    else:
        return -1

def home(request,query=None):
    if not query or query is None:
        return render(request,"short/index.html")
    else:
        try:
            check=shorturl.objects.get(short_name=query)
            check.visit_no+=1
            check.save()
            url_red=check.original_link
            return redirect(url_red)
        except shorturl.DoesNotExist:
            messages.error(request,"404 Not Found")
            return redirect(home)

def Register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        check = request.POST['username'] and request.POST['email'] and request.POST['password1'] and request.POST['password2']
        if not check:
            messages.error(request,"Invalid Credentials")
            return redirect('/register/')
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.error(request,"Username Already exists")
                return redirect('/register/')
            elif User.objects.filter(email=email).exists():
                messages.error(request,"Email Already exists")
                return redirect('/register/')
            else:
                checkpass = passwordcheck(password1)
                if checkpass == -1:
                    messages.error(request,"Password length should be greater than 8")
                    return redirect('/register/')
                elif checkpass == -2:
                    messages.error(request,"Password must have upper and lowercase letter with digits and special characters")
                    return redirect('/register/')
                user=User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                subject = "Welcome to MiniLy"
                messageemail = f"Dear {username},Thank you for registering on MiniLy."
                send_mail(
                    subject,
                    messageemail,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False
                )
                messages.success(request,"Account Created")
                return redirect(home)
        else:
            messages.error(request,"Passwords do not match")
            return redirect('/register/')
    else:    
        return render(request,'short/register.html')

def Login(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            if request.POST['next']!='':
                messages.success(request,"Logged in Successfully")
                return redirect(request.POST['next'])
            messages.success(request,"Logged in Successfully")
            return redirect('/')
        else:
            messages.error(request,"Invalid credentials")
            return redirect('/login/')
    else:
        return render(request,"short/login.html")

def Logout(request):
    if not request.user.is_authenticated:
        return redirect('/')
    logout(request)
    messages.success(request,"Logged out Successfully")
    return redirect('/')

@login_required(login_url="/login/")
def Dashboard(request):
    usr=request.user
    urls=shorturl.objects.filter(user=usr).order_by('-cr_date')
    return render(request,"short/dashboard.html",{
        'urls':urls
    })

@login_required(login_url="/login/")
def generate(request):
    if request.method=='POST':
        if request.POST['original'] and request.POST['short']:
            if len(request.POST['short']) > 15:
                messages.error(request,"Short name cannot have length more than 15")
                return redirect('/dashboard/')
            usr=request.user
            original = request.POST['original']
            short = request.POST['short']
            check = shorturl.objects.filter(short_name=short)
            if not check:
                obj = shorturl(user=usr,original_link=original,short_name=short)
                obj.save()
                messages.success(request,"MiniLy created Successfully")
                return redirect('/dashboard/')
            else:
                messages.error(request, "ShortName Already exists")
                return redirect('/dashboard/')
        elif request.POST['original']:
            usr=request.user
            original = request.POST['original']
            generate_check = False
            while not generate_check:
                short = randomshort()
                check = shorturl.objects.filter(short_name=short)
                if not check:
                    obj = shorturl(user=usr,original_link=original,short_name=short)
                    obj.save()
                    messages.success(request,"MiniLy created Successfully")
                    return redirect('/dashboard/')
                else:
                    continue
        else:
            messages.error(request,"Original URL field empty")
            return redirect('/dashboard/')
    else:
        return redirect('/dashboard/')

@login_required(login_url="/login/")
def edit_minily(request,no):
    if request.method=="POST":
        if request.POST['original'] and request.POST['short']:
            og = request.POST['original']
            sh = request.POST['short']
            ch = shorturl.objects.get(id=no)
            ch.original_link = og
            ch.short_name = sh
            ch.save()
            messages.success(request,"Updated Successfully")
            return redirect('/dashboard/')
        elif request.POST['original']:
            che = shorturl.objects.get(id=no)
            generated = False
            while not generated:
                short = randomshort()
                check1 = shorturl.objects.filter(short_name=short)
                if not check1:
                    che.original_link = request.POST['original']
                    che.short_name = short
                    che.save()
                    messages.success(request,"Updated Successfully")
                    return redirect('/dashboard/')
                else:
                    continue
        else:
            messages.error(request,"Please fill in the value of Original URL")
            return redirect('/dashboard/')
    else:
        check = shorturl.objects.get(id=no)
        if request.user!=check.user:
            messages.error(request,"Access denied")
            return redirect('/dashboard/')
        original = check.original_link
        shorty = check.short_name
        return render(request,"short/editly.html",{
            'original':original,
            "shorty":shorty,
            "id":no
        })

@login_required(login_url="/login/")
def deletely(request,no):
    check = shorturl.objects.get(id=no)
    if request.user!=check.user:
        messages.error(request,"Access denied")
        return redirect('/dashboard/')
    check.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('/dashboard/')


def n_found(request,exception):
    messages.error(request,"404 Page not Found")
    return redirect(home)