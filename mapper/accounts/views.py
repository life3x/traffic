from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from mapperapp.models import registeredWebsite

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect(f'/mapper/{request.user.username}')
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 != password2:
            messages.info(request, "Passwords don't match")
            return redirect('register')
        elif User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('register')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email alreay registered')
            return redirect('register')
        else:
            user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
            user.save()
            return redirect('login')
    else:
        return render(request, 'register.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def profile(request):
    registered_website_json = list(registeredWebsite.objects.filter(username = request.user.username))
    return render(request, 'profile.html', {'registered_sites_number': len(registered_website_json)})

def siteregister(request):
    if request.method == 'POST':
        username = request.user.username
        site = request.POST['url']
        if registeredWebsite.objects.filter(username = username, website = site).exists():
            messages.info(request, 'You have already registered this site')
            return redirect('/accounts/siteregister')
        else:
            registerSite = registeredWebsite.objects.create(username = username, website = site)
            registerSite.save()
            return redirect(f'/integrate')
    return render(request, 'siteregister.html')
