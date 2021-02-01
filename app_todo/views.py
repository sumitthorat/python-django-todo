from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError

def signupuser(request):
    if request.method == 'GET':
        return render(request, 'app_todo/signupuser.html', {'form':UserCreationForm()})
    else:
        # Create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currenttodos')
            except IntegrityError:
                return render(request, 'app_todo/signupuser.html', {'form':UserCreationForm(), 'error':'That username has already been taken.'})
        else:
            return render(request, 'app_todo/signupuser.html', {'form':UserCreationForm(), 'error':'Passwords did not match'})


def currenttodos(request):
    return render(request, 'app_todo/currenttodos.html')

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def home(request):
    return render(request, 'app_todo/home.html')

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'app_todo/loginuser.html', {'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'app_todo/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password did not match'})
        else:
            login(request, user)
            return redirect('currenttodos')