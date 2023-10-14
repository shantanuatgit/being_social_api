from rest_framework.pagination import PageNumberPagination

class ProfilePagination(PageNumberPagination):
    page_size = 30
    page_query_param = 'page'