from drf_yasg import openapi


class AccountSchemas:
    """Schemas for model Account"""

    @classmethod
    def get_output(cls):
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "id": openapi.Schema(type=openapi.TYPE_STRING, description="Id của user"),
            "last_login": openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                                         description="Last login"),
            "is_superuser": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is superuser"),
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First name"),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Last name"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is superuser"),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is superuser"),
            "date_joined": openapi.Schema(
                type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME,
                description="Date joined"
            )
        })

    @classmethod
    def get_input(cls):
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "is_superuser": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is superuser"),
            "username": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "first_name": openapi.Schema(type=openapi.TYPE_STRING, description="First"),
            "last_name": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="Username"),
            "is_staff": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is superuser"),
            "is_active": openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Is superuser"),
            "groups": openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.TYPE_INTEGER, description="Group"),
            "user_permissions": openapi.Schema(
                type=openapi.TYPE_ARRAY, items=openapi.TYPE_INTEGER,
                description="Permission for user"
            )
        })
