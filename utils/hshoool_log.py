from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from rest_framework.request import Request

from hSchool.models import ActivityLog
from models.user import User


def push_activity_log(request: Request, _from=None, _target_id=None, _action=None, _content=None, app_label=None,
                      model_name=None, course_id=None):
    """
    Hschool put activity log
    :request -> request from user
    :_from -> user object
    :_target -> object target
    :_action -> action from user
    :_content -> data activity log
    """
    try:
        user = User.objects.get(pk=_from.id)
        my_model = apps.get_model(app_label=app_label, model_name=model_name)
        title = f'{user.username} {_action} {my_model.objects.filter(pk=_target_id).first().__str__()}'
        c_type = ContentType.objects.get(app_label=app_label, model=model_name.lower())

        ActivityLog.objects.create(
            content_type_id=c_type.id,
            course_id=course_id,
            user_id=request.user.id,
            title=title,
            content=_content,
            target=_target_id
        )
    except (Exception,)as e:
        pass

    return None
