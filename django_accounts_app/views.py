from django.forms import BaseModelForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import CreateView
from django.http import HttpResponse
from server.apps.accounts.forms import CustomUserCreationForm
from django.core.validators import validate_email
from .tasks import mail_send


# Create your views here.
def dashboard(request):
    return render(request, "users/dashboard.html", {})


class RegisterUser(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'users/register.html'

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        user = form.save()
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        validate_email(form.instance.email)
        email = form.instance.email
        username = f'{form.instance.first_name} {form.instance.last_name}'
        subject = 'Welcome to book bot administration'
        mail_send(to_email=email, subject=subject, username=username)

        login(self.request, user)

        return redirect('admin:index')


