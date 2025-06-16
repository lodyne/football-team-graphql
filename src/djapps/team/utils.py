def get_paginated_queryset(queryset, page, page_size):
    """
    Paginate a queryset.
    
    Args:
        queryset: The queryset to paginate.
        page: The page number to retrieve.
        page_size: The number of items per page.
    
    Returns:
        A tuple containing the paginated items and the total count.
    """
    start = (page - 1) * page_size
    end = start + page_size
    return queryset[start:end], queryset.count()

def paginated_queryset(queryset,limit: int, offset: int = 0):
    return queryset[offset:offset + limit]

def get_queryset_with_limit_offset(queryset, limit, offset):
    """
    Retrieve a queryset using limit and offset.

    Args:
        queryset: The queryset to slice.
        limit: The maximum number of items to retrieve.
        offset: The number of items to skip before starting to collect the result set.

    Returns:
        A tuple containing the sliced items and the total count.
    """
    return queryset[offset:offset + limit], queryset.count()