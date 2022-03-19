from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import response, status, permissions
from django.contrib.auth import authenticate
from .jwt import JWTAuthentication



class AuthUserAPIView(GenericAPIView):

    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (JWTAuthentication, )

    def get(self, request):
        user = request.user
        serializer = RegisterSerializer(user)
        return response.Response(
            {
                "user" : serializer.data, 
            }
        )




class RegisterAPIView(GenericAPIView):

    serializer_class = RegisterSerializer
    authentication_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data= request.data)

        if serializer.is_valid():
            serializer.save()

            return response.Response(serializer.data, status= status.HTTP_201_CREATED)
        
        return response.Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
    
class LoginAPIView(GenericAPIView):

    serializer_class = LoginSerializer
    authentication_classes = ()
    
    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username= email, password= password)

        if user:
            serializer = self.serializer_class(user)

            return response.Response(serializer.data, status= status.HTTP_200_OK)
        
        return response.Response(
            {
                "message" : "Invalid Credentials, Try again."
            },
            status= status.HTTP_401_UNAUTHORIZED
        )