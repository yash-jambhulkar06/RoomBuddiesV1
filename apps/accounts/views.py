from django.shortcuts import render,redirect
from .forms import LoginForm ,RegisterForm
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request,"home.html")

def register(request):
    if request.method=="POST":
        form=RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            return redirect("accounts:register")
        
    else:
            form=RegisterForm()
            
    return render(
        request,"accounts/register.html",
            {"form":form},
        )



def login_view(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        
        if form.is_valid():
            email=form.cleaned_data["email"]
            password=form.cleaned_data["password"]
            
            user=authenticate(
                request,
                username=email,
                password=password,
            )
            
            if user is not None:
                login(request,user)
                return redirect("accounts:dashboard")
            
            
    else:
            form=LoginForm()
            
    return render(
        request,"accounts/login.html",
        {"form":form},
    )


@login_required
def dashboard(request):
    context={
        'user':request.user,
    }
    return render(request,"accounts/dashboard.html",context)

def logout_view(request):
    logout(request)
    return redirect("accounts:login")