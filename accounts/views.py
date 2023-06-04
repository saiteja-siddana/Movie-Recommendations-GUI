from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login,logout
from django.http import HttpResponse


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:login')
    else:
        form = UserCreationForm()
    return render(request,"signup.html", {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return redirect('movie_recommendations_app:movies') 
    else:
        form = AuthenticationForm()
    return render(request,"login.html",{'form':form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('movie_recommendations_app:base')
        

