from django.urls import path, include
from .views import dashboard, RegisterUser, success_registration, not_registered
from server.apps.accounts.utils import check_recaptcha

app_name = 'accounts'

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('dashboard/', dashboard, name='dashboard'),
    path('registration/', check_recaptcha(RegisterUser.as_view()), name='registration'),
    path('complete_registration/<str:activation_token>', success_registration, name='success_registration'),
]
