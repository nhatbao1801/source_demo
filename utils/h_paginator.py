from django.core.paginator import Paginator, InvalidPage


def h_paginator(object_list=None, request=None, not_queryset=None):
    """Paginate list of object or queryset
    Args:
        object_list: your query_set or list of objects
        request: your request
        not_queryset: Indicate that your object_list param is not queryset so do not need to sort the result
    """
    if not not_queryset and not object_list.ordered:
        object_list = object_list.order_by('id')

    paginator = Paginator(object_list, request.GET.get('limit') or 10)
    page = request.GET.get('page') or 1
    try:
        current_page = paginator.page(page)
    except InvalidPage as e:
        page = int(page) if page.isdigit() else page
        context = {
            'valid_page': False,
            'page_number': page,
            'message': str(e)
        }
        return [], context
    metadata = {
        'valid_page': True,
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'page_range': [range_page for range_page in paginator.page_range],
        'has_next': current_page.has_next(),
        'has_previous': current_page.has_previous(),
        'current_page': int(page),
        'next_page_number': current_page.next_page_number() if current_page.has_next() else None,
        'previous_page_number': current_page.previous_page_number() if current_page.has_previous() else None
    }
    return current_page, metadata
