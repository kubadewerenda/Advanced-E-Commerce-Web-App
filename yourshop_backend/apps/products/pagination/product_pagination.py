from rest_framework import pagination

class QueryPageNumberPagination(pagination.PageNumberPagination):
    page_size = 3
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 200