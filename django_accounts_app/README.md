# Installation

##*Add to settings.py*

    AUTH_USER_MODEL = 'accounts.CustomUser'

    LOGIN_REDIRECT_URL = '/admin/'
    LOGOUT_REDIRECT_URL = '/accounts/login/'

To INSTALLED_APPS
    
    'server.apps.accounts',

Email settings

```
from server.settings.components import config

ACCOUNT_ACTIVATION_DAYS = 2
EMAIL_TIMEOUT = 20

EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)

EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Is used to set sender name
# https://docs.djangoproject.com/en/1.11/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER
```

## Add to templates

to base.html

    {% block content %}
    {% endblock %}

## Add to .env

```
# ====== Email settings =====

EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=
EMAIL_USE_SSL=
EMAIL_USE_TLS=

# ===== Google Recapthca =====

GOOGLE_RECAPTCHA_SECRET_KEY=
GOOGLE_RECAPTCHA_SECRET_SITE_KEY=
```



## To urls.py

from server.apps.accounts import urls as accounts_urls

url_patterns

    path('accounts/', include(accounts_urls)),
    path('admin/login/', login_required(lambda request: redirect('accounts/login/', permanent=True),
                                        redirect_field_name='admin/login/?next=')),


## Add Google reCaptcha

https://evileg.com/uk/post/283/