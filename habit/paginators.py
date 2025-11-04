from rest_framework.pagination import PageNumberPagination


class PaginationList(PageNumberPagination):
    """
    Пагинация вывода привычек по 5 на страницу.
    """

    page_size = 5
    page_size_query_param = "page_size"
    max_page_size = 10
