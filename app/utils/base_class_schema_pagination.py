import logging
from collections import OrderedDict
from drf_yasg import openapi
from utils.base_schemas import metadata_paginator

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)
from drf_yasg.inspectors import PaginatorInspector


class PaginatorInspectorClass(PaginatorInspector):

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

    
    def get_paginated_response(self, paginator, response_schema):
        """
        :param BasePagination paginator: the paginator
        :param openapi.Schema response_schema: the response schema that must be paged.
        :rtype: openapi.Schema
        """

        return openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties=OrderedDict((
                ('data', response_schema),
                ('metadata', metadata_paginator())
            ))
        )