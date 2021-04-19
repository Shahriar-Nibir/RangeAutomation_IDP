from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import *
from .decorators import *

# Create your views here.


@unauthenticated_user
def home(request):
    return render(request, 'home.html')


@unauthenticated_user
def loginUser(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == 'Unit-User':
                    return redirect('inputfirer')
                elif group == 'Range-Admin':
                    return redirect('adddetail')
            else:
                return render(request, 'invalid.html')
        else:
            messages.info(request, "User with this credentials doesn't exist.")
    return render(request, 'login.html')


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@unauthenticated_user
def aboutus(request):
    return render(request, 'aboutus.html')


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def showmember(request):
    firer = Firer.objects.all()
    context = {'firer': firer}
    return render(request, 'showmember.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
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


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def firingresult(request):
    firer = None
    if request.method == 'POST':
        number = request.POST['number']
        try:
            firer = Firer.objects.get(number=number)
            return redirect('result', pk=firer.id)
        except:
            messages.warning(
                request, "Person with this number doesnot exits. May be you have typed something wrong.")
    context = {}
    return render(request, 'firingresult.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Unit-User'])
def result(request, pk):
    firer = Firer.objects.get(id=pk)
    result = Result.objects.filter(firer=firer)
    context = {'firer': firer, 'result': result}
    return render(request, 'result.html', context)


@login_required(login_url='login')
@allowed_user(allowed_role=['Range-Admin'])
def adddetail(request):
    context = {}
    return render(request, 'adddetail.html', context)
