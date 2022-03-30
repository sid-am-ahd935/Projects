# from django.shortcuts import render
# # from rest_framework.decorators import api_view
# from rest_framework import status
from posts.models import Post
from posts.serializers import PostSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework import permissions
from posts.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response


# from rest_framework.views import APIView
# from django.http import Http404


@api_view(["GET"])
def api_root(request, format= None):
    return Response(
        {
            'users': reverse('user-list', request= request, format= format),
            'posts': reverse('post-list', request= request, format= format)
        }
    )


# @api_view(["GET", "POST"])
# def post_list(request, format= None):
#     if request.method == "GET":
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many= True)
#         return Response(serializer.data)


#     elif request.method == "POST":
#         serializer = PostSerializer(data= request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
        
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', "POST", 'DELETE', "PUT"])
# def post_detail(request, pk, format= None):
#     try:
#         post = Post.objects.get(pk= pk)
#     except Post.DoesNotExist:
#         return Response(status= status.HTTP_404_NOT_FOUND)
    
#     if request.method == "GET":
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     elif request.method == "POST":
#         data = JsonParser().parse(request)
        
#         if serializer.is_valid():
#             serializer.save()

#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status= 400)
    
#     elif request.method == "PUT":
#         serializer = PostSerializer(post, data= request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
#     elif request.method == "DELETE":
#         post.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT, format= None)


####            Class based views for the same functionality above

# class PostList(APIView):

#     def get(self, request, format= None):
#         posts = Post.objects.all()
#         serializer = PostSerializer(posts, many= True)
#         return Response(serializer.data)
    
#     def post(self, request, format= None):
#         serializer = PostSerializer(data= request.data)

#         if serializer.is_valid():
#             serialzer.save()
#             return Response(serializer.data, status= status.HTTP_201_CREATED)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             post = Post.objects.get(pk= pk)
#         except Post.DoesNotExist:
#             # return Response(status= status.HTTP_404_NOT_FOUND)
#             raise Http404
#         return post

        
#     def get(self, request, pk, format= None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     def put(self, request, pk, format= None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data= request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format= None):
#         post = self.get_object(pk)
#         post.delete()
#         return Response(status= status.HTTP_204_NO_CONTENT)

#### For more shorter code use mixins classes
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# from rest_framework.generics import GenericAPIView

# class PostList(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

    
# class PostDetail(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


##### CLass based generics rocksss!!!
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import generics

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostList(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]

    def perform_create(self, serializer):
        serializer.save(owner= self.request.user)


class PostDetail(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]