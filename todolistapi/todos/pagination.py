from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 2                              # Default page size if page size (denoted by page_size_query_param, here count) is not present
    page_size_query_param = "count"            # Page Size of the requested page
    max_page_size = 30                         # Maximum page size
    page_query_param = "p"                     # Query Parameter Name for getting a page

