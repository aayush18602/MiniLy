from django.conf.urls import url
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Tree
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.

@login_required(login_url="/login/")
def index(request):
    user=request.user
    mytree = Tree.objects.filter(user=user)
    return render(request,"tree/home.html",{
        'elements':mytree,
        'user':user
    })

def create(request):
    if request.method=="POST":
        if request.POST['Treename'] and request.POST['URL']:
            usr=request.user
            name = request.POST['Treename']
            url_tree = request.POST['URL']
            obj = Tree(user=usr,original_link=url_tree,short_name=name)
            obj.save()
            messages.success(request,"Created Successfully")
            return redirect('/t/')
        else:
            print(request.POST)
            messages.error(request,"Empty field")
            return redirect('/t/')
    else:
        return redirect('/t/')


def treelink(request,query):
    user = User.objects.get(username= query)
    mytree = Tree.objects.filter(user=user)
    if mytree:
        return render(request,"tree/treelinks.html",{
            "elements":mytree,
            "username":query
        })
    else:
        return render(request,"tree/treelinks.html")

@login_required(login_url="/login/")
def edittree(request,no):
    if request.method=="POST":
        if request.POST['URL'] and request.POST['Treename']:
            og = request.POST['URL']
            sh = request.POST['Treename']
            ch = Tree.objects.get(id=no)
            ch.original_link = og
            ch.short_name = sh
            ch.save()
            messages.success(request,"Updated Successfully")
            return redirect('/t/')
        else:
            messages.error(request,"Please fill in the values")
            return redirect('/t/')
    else:
        check = Tree.objects.get(id=no)
        if request.user!=check.user:
            messages.error(request,"Access denied")
            return redirect('/t/')
        original = check.original_link
        shorty = check.short_name
        return render(request,"tree/edittree.html",{
            'original':original,
            "shorty":shorty,
            "id":no
        })

@login_required(login_url="/login/")
def deletree(request,no):
    check = Tree.objects.get(id=no)
    if request.user!=check.user:
        messages.error(request,"Access denied")
        return redirect('/t/')
    check.delete()
    messages.success(request,"Deleted Successfully")
    return redirect('/t/')
    
