from drf_yasg import openapi


def metadata_paginator():
    return openapi.Schema(type=openapi.TYPE_OBJECT, properties={
        'valid_page': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'count': openapi.Schema(type=openapi.TYPE_INTEGER),
        'num_pages': openapi.Schema(type=openapi.TYPE_INTEGER),
        'page_range': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
        'has_next': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'has_previous': openapi.Schema(type=openapi.TYPE_BOOLEAN),
        'current_page': openapi.Schema(type=openapi.TYPE_INTEGER),
        'next_page_number': openapi.Schema(type=openapi.TYPE_INTEGER),
        'previous_page_number': openapi.Schema(type=openapi.TYPE_INTEGER),
    })
