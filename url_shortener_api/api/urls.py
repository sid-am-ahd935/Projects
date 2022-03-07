from django.urls import path
from . import views 

urlpatterns = [
    path("", views.ShortenerListAPIView.as_view(), name='all-links'),
    path("create/", views.ShortenerCreateAPIView.as_view(), name= "create_api"),

]