from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *

# Create your views here.


def home(request):
    return render(request, 'home.html')


def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inputfirer')
        else:
            messages.info(request, "User with this credentials doesn't exist.")
    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


def aboutus(request):
    return render(request, 'aboutus.html')


@login_required(login_url='login')
def showmember(request):
    firer = Firer.objects.all()
    context = {'firer': firer}
    return render(request, 'showmember.html', context)


@login_required(login_url='login')
def inputfirer(request):
    form = FirerForm()
    if request.method == 'POST':
        form = FirerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, "New Firer Created.")
        else:
            messages.warning(
                request, "Wrong Credentials. Firer already exists with this credentials.")
    context = {'form': form}
    return render(request, 'inputfirer.html', context)
