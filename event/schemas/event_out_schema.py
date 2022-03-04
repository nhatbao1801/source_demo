from drf_yasg.openapi import Schema, TYPE_STRING, TYPE_OBJECT, TYPE_INTEGER, FORMAT_URI, TYPE_ARRAY, TYPE_BOOLEAN


class EventOutSchema:
    """ This is schema of class serializer base EventOutSerializer """
    @classmethod
    def get_schema(cls):
        return Schema(type=TYPE_OBJECT, properties={
            'id': Schema(type=TYPE_INTEGER),
            'picture': Schema(type=TYPE_STRING, format=FORMAT_URI),
            'areas_info': Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                'id': Schema(type=TYPE_INTEGER),
                'name': Schema(type=TYPE_STRING)
            })),
            'city_info': Schema(type=TYPE_OBJECT, properties={
                'id': Schema(type=TYPE_INTEGER),
                'name': Schema(type=TYPE_STRING)
            }),
            'type_info': Schema(type=TYPE_OBJECT, properties={
                'id': Schema(type=TYPE_INTEGER),
                'name': Schema(type=TYPE_STRING)
            }),
            'object_creation': Schema(type=TYPE_OBJECT, properties={
                'name': Schema(type=TYPE_STRING),
                'picture': Schema(type=TYPE_STRING),
                'url': Schema(type=TYPE_STRING)
            }),
            'areas_id': Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_INTEGER)),
            'city_id': Schema(type=TYPE_INTEGER),
            'event_type_id': Schema(type=TYPE_INTEGER),
            'cover': Schema(type=TYPE_STRING, format=FORMAT_URI),
            'is_edit': Schema(type=TYPE_BOOLEAN),
            'ticket_info': Schema(type=TYPE_OBJECT, properties={
                'id': Schema(type=TYPE_STRING),
                'timezone_info': Schema(type=TYPE_OBJECT, properties={
                    'id': Schema(type=TYPE_INTEGER),
                    'value': Schema(type=TYPE_STRING),
                    'text': Schema(type=TYPE_STRING),
                    'gmt': Schema(type=TYPE_STRING),
                }),
                'name': Schema(type=TYPE_STRING),
                'description': Schema(type=TYPE_STRING),
                'sale_from': Schema(type=TYPE_STRING),
                'sale_to': Schema(type=TYPE_STRING),
                'max_quantity': Schema(type=TYPE_STRING),
                'sold': Schema(type=TYPE_STRING),
                'price': Schema(type=TYPE_STRING),
            }),
            'participants': Schema(type=TYPE_OBJECT, properties={
                'users': Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_INTEGER)),
                'teams': Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_INTEGER)),
            }),
            'sponsor_info': Schema(type=TYPE_ARRAY, items=Schema(type=TYPE_OBJECT, properties={
                'id': Schema(type=TYPE_INTEGER),
                'name': Schema(type=TYPE_STRING)
            })),
            'application_info': Schema(type=TYPE_INTEGER),
            'application_form_info': Schema(type=TYPE_INTEGER),
        })