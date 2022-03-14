from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_INTEGER, TYPE_STRING, TYPE_BOOLEAN


class LecturerSerializerSchema:
    """" This is Schema for LecturerSerializer class"""
    @classmethod
    def get_schema(cls):
        return Schema(type=TYPE_OBJECT, properties={
            'user': Schema(type=TYPE_INTEGER),
            'title': Schema(type=TYPE_STRING),
            'description': Schema(type=TYPE_STRING),
            'email': Schema(type=TYPE_STRING),
            'is_admin_accept': Schema(type=TYPE_BOOLEAN),
            'date_admin_accepted': Schema(type=TYPE_STRING),
            'created_by': Schema(type=TYPE_INTEGER),
            'updated_by': Schema(type=TYPE_INTEGER),
            'created_at': Schema(type=TYPE_STRING),
            'updated_at': Schema(type=TYPE_STRING),
        })