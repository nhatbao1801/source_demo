from drf_yasg import openapi


class CourseSubCategorySchema:

    @classmethod
    def data_in_schema(cls):
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='id of category'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='name of subcategory'),
            'thumb': openapi.Schema(type=openapi.TYPE_FILE, description='thumb of subcategory'),
            'area': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_STRING, description='areas')
            )
        })

    @classmethod
    def data_out_schema(cls):
        return openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            "id": openapi.Schema(type=openapi.TYPE_INTEGER),
            'category_info': openapi.Schema(type=openapi.TYPE_INTEGER),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'thumb_url': openapi.Schema(type=openapi.TYPE_FILE),
            'area_info': openapi.Schema(
                type=openapi.TYPE_ARRAY,
                items=openapi.Schema(type=openapi.TYPE_OBJECT, properties={
                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                    'name': openapi.Schema(type=openapi.TYPE_STRING)
                })
            )
        })
