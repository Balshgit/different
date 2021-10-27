from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.http import HttpResponse, HttpRequest
from server.apps.accounts.forms import CustomUserCreationForm
from server.apps.accounts.models import CustomUser
from django.core.validators import validate_email
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings


def dashboard(request: HttpRequest) -> HttpResponse:
    return render(request, "users/dashboard.html", {})


def not_registered(request: HttpRequest) -> HttpResponse:
    return redirect('accounts:login')


def success_registration(request: HttpRequest, activation_token: str) -> HttpResponse:
    try:
        user = CustomUser.objects.get(activation_token=activation_token)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        user.is_staff = True
        user.activation_token = ''
        user.save()
        login(request, user)
        return redirect('admin:index')
    except ObjectDoesNotExist:
        message = 'Activation token not found'
        return render(request, 'registration/info.html', {'message': message}, status=404)


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        if self.request.recaptcha_is_valid:
            user = form.save()
            validate_email(form.instance.email)
            if settings.CONFIRM_REGISTRATION_BY_EMAIL:
                message = 'Please check your email for continue registration'
                return render(self.request, 'registration/info.html', {'message': message})
            else:
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(self.request, user)
                return redirect('admin:index')
        return render(self.request, 'users/register.html', self.get_context_data())
