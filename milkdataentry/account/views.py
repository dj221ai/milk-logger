from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic.edit import FormView, CreateView
from .models import CustomUser
from .forms import (RegistrationForm, LoginForm,
                    CustomUserAdminChangeForm, CustomUserAdminCreationForm)


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def form_valid(self, form):
        request = self.request
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        try:
            if user is not None:
                login(request, user)
                return redirect('loggingDailyData:daily_total')
        except Exception as e:
            print('error is ', e)
        return super(LoginView, self).form_invalid(form)


class SignUpView(CreateView):
    form_class = RegistrationForm
    template_name = 'account/register.html'
    success_url = '/account/login/'


def logout_view(request):
    logout(request)
    return redirect('/')
