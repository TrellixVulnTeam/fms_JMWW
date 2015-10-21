from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponseRedirect
from builder.forms import SignupForm, LoginForm


class SignupView(View):
    def get(self, request, *args, **kwargs):
        signup_form = SignupForm()
        return render(request, 'signup.html', {
            'signup_form': signup_form
        })

    def post(self, request, *args, **kwargs):
        signup_form = SignupForm(request.POST)
        if not signup_form.is_valid():
            return render(
                request, 'signup.html', {
                    'signup_form': signup_form
                },
                status=400
            )
        logout(request)
        signup_form.create_user()
        new_user = authenticate(
            username=signup_form.cleaned_data['username'],
            password=signup_form.cleaned_data['password'],
        )
        #@TODO from settings
        request.session.set_expiry(60*60*24*7)
        #@TODO from settings
        return redirect('account')


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('index')
        login_form = LoginForm()
        return render(request, 'login.html', {
            'login_form': login_form
        })

    def post(self, request, *args, **kwargs):
        login_form = LoginForm(request.POST)
        if not login_form.is_valid():
            return render(
                request, 'login.html', {
                    'login_form': login_form
                },
                status=400
            )
        user = login_form.get_user()
        login(request, user)
        #@TODO from settings
        request.session.set_expiry(60*60*24*7)
        #@TODO from settings
        return redirect('account')
