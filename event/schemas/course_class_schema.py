from drf_yasg.openapi import Schema, TYPE_INTEGER, TYPE_STRING, TYPE_BOOLEAN, TYPE_OBJECT, TYPE_ARRAY, FORMAT_DATE


class CourseClassSchemas:
    """"This is schema for model CourseClass"""
    @classmethod
    def get_schema(cls):
        return Schema(type=TYPE_OBJECT, properties={
            'id': Schema(type=TYPE_INTEGER),
            'course': Schema(type=TYPE_INTEGER),
            'lecturer': Schema(type=TYPE_INTEGER),
            'students': Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_INTEGER)),
            'title': Schema(type=TYPE_STRING),
            'start_date': Schema(type=TYPE_STRING, format=FORMAT_DATE),
            'schedule': Schema(type=TYPE_STRING),
            'address': Schema(type=TYPE_STRING),
        })