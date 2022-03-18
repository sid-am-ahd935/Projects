from django.shortcuts import render
from rest_framework import permissions, filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
# from rest_framework.generics import CreateAPIView, ListAPIView  # Not using these
from .serializers import TodoSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Todo
from django_filters.rest_framework import DjangoFilterBackend
from .pagination import CustomPageNumberPagination
# Create your views here.


class TodosAPIView(ListCreateAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, )
    pagination_class = CustomPageNumberPagination
    queryset = Todo.objects.all()

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["id", "title", "is_complete"]
    search_fields = ["id", "title", "desc", "is_complete"]
    ordering_fields = ["id", "title", "desc", "is_complete"]

    def perform_create(self, serializer):
        return serializer.save(owner= self.request.user)

    def get_queryset(self):
        return Todo.objects.filter(owner= self.request.user)

class TodoDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated, )
    lookup_field = "id"


    def get_queryset(self):
        return Todo.objects.filter(owner= self.request.user)

## Same functionality as TodosAPIView but broken down into different class views
# class CreateTodoAPIView(CreateAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = (IsAuthenticated, )

#     def perform_create(self, serializer):
#         return serializer.save(owner= self.request.user)

# class TodoListAPIView(ListAPIView):
#     serializer_class = TodoSerializer
#     permission_classes = (IsAuthenticated, )

#     queryset = Todo.objects.all()


#     def get_queryset(self):
#         return Todo.objects.filter(owner= self.request.user)