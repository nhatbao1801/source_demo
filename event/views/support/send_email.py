from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# from hSpace import settings
from django.conf import settings


def owner_event_send_thanks(data=None):
    subject = _("Notification from hspaces.net")
    reply_to = settings.DEFAULT_FROM_EMAIL
    body = render_to_string('event/email/email_owner_send_thanks.html',
                            {
                                # 'owner_name': data['owner_name'],  # Nga comment
                                'event_name': data['event_name'],
                                'event_url': data['event_url']
                            })
    create_email = EmailMessage(subject=subject, body=body, to=[data['owner_team_mail']], reply_to=[reply_to])
    create_email.content_subtype = 'html'
    create_email.send(fail_silently=True)


def team_or_user_send_join_event(data=None):
    subject = _("Notification from hspaces.net")
    reply_to = settings.DEFAULT_FROM_EMAIL
    body = render_to_string('event/email/team_or_user_send_join_event.html',
                            {
                                # 'owner_name': data['owner_name'],  # Nga comment
                                'event_name': data['event_name'],
                                'event_url': data['event_url'],
                                'team_or_user_name': data['team_or_user_name'],
                            })
    create_email = EmailMessage(subject=subject, body=body, to=[data['owner_team_mail']], reply_to=[reply_to])
    create_email.content_subtype = 'html'
    create_email.send(fail_silently=True)
