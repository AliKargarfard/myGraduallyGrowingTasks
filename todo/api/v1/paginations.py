from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

# class LargeResultsSetPagination(PageNumberPagination):
#     page_size = 6
#     page_size_query_param = 'page_size'
#     max_page_size = 20

'''  سفارشی سازی صفحه بندی '''
class CustomPagination(PageNumberPagination):
    page_size = 3
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'total_tasks': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })
