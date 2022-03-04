#  Copyright (c) 2020
#  Team hspaces.net
#  Contributors sang.tanhle, HuynhDH
import json
import logging
import os
from datetime import datetime, timedelta

import requests
from django.conf import settings
from firebase_admin import messaging

from models import (UserNotificationSetting, Notification, User)
from models.device import Device

# Config logger for logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

logger_in_signal_file_path = os.path.join(os.path.join(settings.BASE_DIR, 'logs'), 'common__signal.log')

file_handler = logging.FileHandler(logger_in_signal_file_path)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def send_notification(
        _type: str = None,
        from_user: int = None,
        to_user=None,
        location: str = None,
        title: str = None,
        content: str = None,
        image: str = None,
        link: str = None
):
    """Send notification through FCM and Websocket microservice

    Args:
        _type: "system", "matched_job", "profile_viewer", "new_message", "follower", "new_reviewed"
        from_user: Source user who send the notification, no need if _type is system
        to_user: Target user receive notification
        location: Where the notification come from like hschool, hstartup, htransformation, system
        title: Title of the notification
        content: Content of the notification
        image: Link of the image of notification
        link: Link for redirection when click to the notification
    """
    user_devices_tokens = [
        dev_token for dev_token in
        Device.objects.filter(user_id=to_user).values_list('device_registration_token_fcm', flat=True)
    ]

    if len(user_devices_tokens) == 0:
        logger.warning('No devices token found to send notification')

    # Check type send token
    is_turn_on = None
    data = {
        'title': str,
        'body': str
    }
    if _type == 'system':
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='rsun#98',
                                                            state=True).exists()
        data['title'] = title or 'New feature updated!'
        data['body'] = content or 'Some features, bugs fixed has been already updated!'
    elif _type == 'matched_job':
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='njm#98',
                                                            state=True).exists()
        data['title'] = title or 'Job Job Job!'
        data['body'] = content or 'Some job matched your profile!'
    elif _type == 'profile_viewer':
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='pv#98',
                                                            state=True).exists()
        data['title'] = title or 'Your profile!'
        data['body'] = content or 'Your profile has been viewed!'
    elif _type == 'new_message':
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='hnm#98',
                                                            state=True).exists()
        data['title'] = title or 'New Message!'
        data['body'] = content or 'You have a new message'

    elif _type == 'follower':
        data['title'] = title or 'New follower!'
        data['body'] = content or 'You have a new follower'
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='hnf#98',
                                                            state=True).exists()
    elif _type == 'preference':
        data['title'] = title or 'New Preference'
        data['body'] = content or 'You have new preference by other'
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='prefer#98',
                                                            state=True).exists()
    elif _type == 'course_approval':
        data['title'] = title or 'New course approval request'
        data['body'] = content or 'You have new request for course approval'
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='coapr#98',
                                                            state=True).exists()
    elif _type == 'new_reviewed':
        data['title'] = title or 'New reviewed by student'
        data['body'] = content or 'You have new reviewed by student'
        is_turn_on = UserNotificationSetting.objects.filter(user_id=to_user, notification_setting__code='newre#98',
                                                            state=True).exists()

    if is_turn_on:
        notification = messaging.Notification(
            title=data.get('title'),
            body=data.get('body'),
            image=image or 'https://hspaces.net/static/media/logo-hspace.5c058243.svg'
        )
        # android
        android = messaging.AndroidConfig(
            ttl=timedelta(seconds=3600),
            priority='normal',
            notification=messaging.AndroidNotification(title=data.get('title'), body=data.get('body')),
        )
        # web push
        web_push = messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                title=data.get('title'), body=data.get('body'),
                icon='https://hspaces.net/static/media/logo-hspace.5c058243.svg',
            ),
        )
        # apns
        apns = messaging.APNSConfig(
            headers={'apns-priority': '10'},
            payload=messaging.APNSPayload(
                aps=messaging.Aps(
                    alert=messaging.ApsAlert(title=data.get('title'), body=data.get('body')),
                    badge=42,
                ),
            ),
        )
        today = datetime.today().strftime('%Y-%d-%m %H:%M:%S')
        # Create notification and save to database
        notification_info = Notification(
            sender_id=from_user if from_user else None,
            user_id=to_user,
            content=content if content else 'No content',
            type=_type if _type else 'No type',
            location=location if location else 'No location'
        )
        notification_info.save()
        message = messaging.MulticastMessage(
            data={
                'id': f'{notification_info.id}',
                'datetime': f'{today}',
                'content': notification_info.content,
                'link': link or 'https://hspaces.net'
            },
            notification=notification,
            android=android,
            webpush=web_push,
            apns=apns,
            tokens=user_devices_tokens,
        )
        response = messaging.send_multicast(message)
        # Send notification through websocket microservice
        data = None
        if from_user:
            from_user = None
            try:
                from_user = User.objects.get(pk=from_user)
            except User.DoesNotExist:
                pass
            data = {
                "payload": {
                    "id": f"{notification_info.id}",
                    "username": from_user.username if from_user else None,
                    "avatar": from_user.picture.build_url(secure=True) if from_user and from_user.picture else None,
                    "content": f"{notification_info.content} - link",
                    "datetime_sent": f"{notification_info.datetime_sent.strftime('%Y-%m-%dT%H:%M:%S.%f')}"
                },
                "message": f"{notification_info.message}",
                "type": f"{notification_info.type}",
                "location": f"{notification_info.location}",
                "user_id": f"{notification_info.user.id}"
            }
        elif _type == 'system':
            data = {
                "payload": {
                    "id": f"{notification_info.id}",
                    "username": "System",
                    "avatar": "https://hspaces.net/static/media/logo-hspace.5c058243.svg",
                    "content": f'{notification_info.content} - link',
                    "datetime_sent": notification_info.datetime_sent.strftime('%Y-%m-%dT%H:%M:%S.%f')
                },
                "message": f"{notification_info.message}",
                "type": f"{notification_info.type}",
                "location": f"{notification_info.location}",
                "user_id": notification_info.user.id
            }
        requests.post('https://chat.hspaces.net/sys/noti/', data=json.dumps(data))
        if response.failure_count > 0:
            responses = response.responses
            failed_tokens = []
            for idx, resp in enumerate(responses):
                if not resp.success:
                    # The order of responses corresponds to the order of the registration tokens.
                    failed_tokens.append(user_devices_tokens[idx])
            logger.warning('List of tokens that caused failures: {0}'.format(failed_tokens))
        return True
    return False