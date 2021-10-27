
from django.urls import path, include
from .views import dashboard, RegisterUser

app_name = 'accounts'

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('dashboard/', dashboard, name='dashboard'),
    path('registration/', RegisterUser.as_view(), name='registration')
]
