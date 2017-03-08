from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from .models import User
import types

# displays a page where user can either register or log in
def index(request):
    return render(request, 'login_registration/index.html')

# registers user name, email, and password if all information is valid
def register(request):
    if request.method != 'POST':
        return redirect(reverse('login_registration:index'))
    else:
        user = User.objects.register(request.POST)
        if isinstance(user, types.ListType):
            for error in user:
                messages.error(request, error)
            return redirect(reverse('login_registration:index'))
        else:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            messages.success(request, "Successfully registered!")
            print "Here!"
            return redirect(reverse('wish_list:dashboard'))

# logs in user if user information is valid and saves information into a session
def login(request):
    if request.method != 'POST':
        return redirect(reverse('login_registration:index'))
    else:
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid Username or Password!")
            return redirect(reverse('login_registration:index'))
        else:
            request.session['user_id'] = user.id
            request.session['first_name'] = user.first_name
            request.session['last_name'] = user.last_name
            messages.success(request, "Successfully logged in!")
            return redirect(reverse('wish_list:dashboard'))

# logs out a user and deletes session containing user information
def logout(request):
    User.objects.logout(request.session['user_id'])
    messages.success(request, "Successfully logged out!")
    return redirect(reverse('login_registration:index'))
