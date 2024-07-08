from collections import OrderedDict
from rest_framework.response import Response
from rest_framework import pagination


class PageNumberPagination(pagination.PageNumberPagination):
    page_query_param = "page"
    page_size_query_param = "pageSize"

    def __init__(self, *args, **kwargs):
        super(*args, **kwargs)
        print("调用django的返回格式")

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('itemCount', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('list', data)
        ]))
