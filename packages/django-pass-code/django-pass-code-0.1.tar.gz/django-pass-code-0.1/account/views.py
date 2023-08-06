from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import auth
from django.contrib.auth.decorators import login_required

from .forms import (PhoneForm, PassCodeForm)
from .utils import generate_pass_code, send_message
from .models import User


def login(request):
    data = {'result': False}
    form = PhoneForm(request.POST or None)
    if form.is_valid():
        phone = form.cleaned_data.get('phone')
        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            return JsonResponse(data)
        pass_code = str(generate_pass_code())
        user.set_password(pass_code)
        user.save()
        # send_message(phone, pass_code)
        print(pass_code)
        request.session['phone'] = phone
        return redirect('account:verify')
    ctx = {
        'form': form,
    }
    return render(request, 'account/form.html', ctx)


def verify(request):
    data = {'result': False}
    form = PassCodeForm(request.POST or None)
    if form.is_valid():
        phone = request.session['phone']
        password = form.cleaned_data.get('pass_code')
        user = auth.authenticate(phone=phone, password=password)
        if user:
            auth.login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
        else:
            return JsonResponse(data)
    ctx = {
        'form': form,
    }
    return render(request, 'account/verify.html', ctx)


@login_required
def logout(request):
    auth.logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def signup(request):
    form = PhoneForm(request.POST or None)
    if form.is_valid():
        phone = form.cleaned_data.get('phone')
        user, created = User.objects.get_or_create(phone=phone)
        pass_code = str(generate_pass_code())
        user.set_password(pass_code)
        user.save()
        # send_message(phone, pass_code)
        print(pass_code)
        request.session['phone'] = phone
        return redirect('account:verify')
    ctx = {
        'form': form,
    }
    return render(request, 'account/form.html', ctx)
