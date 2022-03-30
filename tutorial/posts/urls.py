from django.urls import path
from posts import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns= [
    # path("posts/", views.post_list),
    # path("posts/<int:pk>/", views.post_detail),
    path("posts/", views.PostList.as_view(), name= "post-list"),
    path("posts/<int:pk>/", views.PostDetail.as_view(), name= "post-detail"),
    path("users/", views.UserList.as_view(), name= "user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name= "user-detail"),
    path("", views.api_root, name= "root")
]

urlpatterns = format_suffix_patterns(urlpatterns)