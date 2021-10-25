from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string


@shared_task
def mail_send(to_email: str, subject: str, text_content: str = '', **kwargs) -> None:

    username = kwargs.get('username')
    from_email = settings.DEFAULT_FROM_EMAIL

    msg_html = render_to_string('registration/message.html',
                                {'username': username})

    send_mail(subject, text_content, from_email, [to_email], html_message=msg_html, fail_silently=False)
