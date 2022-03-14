from drf_yasg import openapi


class CourseCategorySchema:

    @classmethod
    def data_schema(cls):
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='id of type'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='name of category'),
            'thumb': openapi.Schema(type=openapi.TYPE_STRING, description='thumb of category')
        })

    @classmethod
    def out_schema(cls):
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            "name": openapi.Schema(type=openapi.TYPE_STRING),
            "thumb_url": openapi.Schema(type=openapi.TYPE_STRING),
            "type_info": openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                'name': openapi.Schema(type=openapi.TYPE_STRING)
            })
        })
