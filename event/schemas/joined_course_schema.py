from drf_yasg.openapi import Schema, TYPE_STRING, TYPE_INTEGER, TYPE_OBJECT, FORMAT_DATETIME


class JoinedCourseSchema:
    """"This is schemas for model JoinedCourse"""
    @classmethod
    def get_schema(cls):
        return Schema(type=TYPE_OBJECT, properties={
            'id': Schema(type=TYPE_INTEGER),
            'payment_status': Schema(type=TYPE_STRING,
                                     enum=['Unpaid', 'Failed', 'Expired', 'PAID', 'Refunding', 'Refunded']),
            'date_joined': Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
            'date_payment_failed': Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
            'date_payment_paid': Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
            'date_payment_refunded': Schema(type=TYPE_STRING, format=FORMAT_DATETIME),
            'user': Schema(type=TYPE_INTEGER),
            'course': Schema(type=TYPE_INTEGER),
        })
