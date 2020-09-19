from email.policy import HTTP

from django.contrib.auth import authenticate, login, user_logged_in, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse


def login_view(request):
    # if user_logged_in:
    #     return HttpResponseRedirect(reverse('accounts:panel'))
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context = {
                'username': username,
                'error': 'نام کاربری یا رمز عبور اشتباه است!',
            }
        else:
            login(request, user)
            return HttpResponseRedirect(reverse('accounts:profile'))
    elif request.user.is_authenticated:
        return HttpResponseRedirect(reverse('accounts:profile'))
    else:
        context = {}
    return render(request, 'accounts/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))


@login_required
def profile_view(request):
    profile = request.user.profile
    context = {
        'profile': profile,
    }
    return render(request, 'accounts/profile.html', context)
