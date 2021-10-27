from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
from django.dispatch import receiver
from django.conf import settings
from .tasks import mail_send
from server.settings.components.logging import main_logger


class CustomUser(AbstractUser):

    mobile = models.CharField(max_length=15, null=True, blank=True, unique=True,
                              help_text='Users mobile phone')
    verification_code = models.CharField(max_length=10, unique=True, null=True, blank=True,
                                         help_text='Verification code for bot account')
    user_created = models.DateField(editable=False, auto_now_add=True, verbose_name='User created',
                                    help_text='Date when user has been created')
    activation_token = models.CharField(max_length=20, null=True, blank=True,
                                        help_text='Activation token for any user')
    email = models.EmailField(max_length=30, unique=True, blank=False, null=True, help_text='User email')
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    def __str__(self):
        return self.username


def user_tokens() -> dict:
    tokens_dict = dict()

    def generate_token(token_length: int) -> str:
        from random import choice
        token_chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
        generated_token = ''
        for i in range(token_length):
            generated_token += choice(token_chars)
        return generated_token

    tokens_dict['activation_token'] = generate_token(token_length=20)
    tokens_dict['verification_code'] = generate_token(token_length=10)
    try:
        users = CustomUser.objects.all().values('activation_token', 'verification_code')
        for user in users:
            if tokens_dict['activation_token'] == user['activation_token']:
                tokens_dict['activation_token'] = generate_token(token_length=20)
            if tokens_dict['verification_code'] == user['verification_code']:
                tokens_dict['verification_code'] = generate_token(token_length=10)
        return tokens_dict
    except Exception as e:
        main_logger.error(f'Cant create tokens because they are not unique. '
                          f'Activation token: {tokens_dict["activation_token"]} '
                          f'Verification code:{tokens_dict["verification_code"]}'
                          f'\nError: {e}')


# # Send email to user
@receiver(models.signals.post_save, sender=CustomUser)
def send_activation_letter(sender, instance, created, **kwargs):
    if created and instance.username != 'admin':
        username = f'{instance.first_name} {instance.last_name}'
        subject = 'Welcome to book bot administration'
        email = instance.email
        try:
            if settings.CONFIRM_REGISTRATION_BY_EMAIL:
                instance.activation_token = user_tokens()['activation_token']
                instance.verification_code = user_tokens()['verification_code']
                instance.save()
                user = CustomUser.objects.get(username=instance.username)
                text = f'https://{settings.DOMAIN_NAME}/accounts/complete_registration/{user.activation_token}'
                mail_send(to_email=email, subject=subject, username=username, text_content=text)
            else:
                instance.is_staff = True
                mail_send(to_email=email, subject=subject, username=username)
        except Exception as e:
            main_logger.error(f'Email not send to user {instance.username}. Reason: {e}')
