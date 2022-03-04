#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH, DuongNV
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from hSpace import settings


def h_send_email(data: object, receiver_email: str):
    """Function send email
    Args:
        data: (obj): Request object
        receiver_email: (str): receiver email
    """

    subject = f'HSPACES.NET - {data["subject"] if "subject" in data.keys() else ""}'
    reply_to = settings.DEFAULT_FROM_EMAIL
    body = render_to_string('challenge/email/email_notifications_have_solution_submit.html',
                            {
                                'challenge_name': data['challenge_name'],
                            })
    request_activate_mail = EmailMessage(subject=subject, body=body, to=[receiver_email],
                                         reply_to=[reply_to])
    request_activate_mail.content_subtype = 'html'
    request_activate_mail.send(fail_silently=True)
