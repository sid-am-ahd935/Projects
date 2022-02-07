from jose import jwt
import datetime
from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .serializers import UserSerializer, PasswordResetRequestByEmailSerializer
from .models import User
from .utils import Util, allowed_users
# Create your views here.

def home(request):
    return render(request, "home.html")

@allowed_users(allowed_roles=["student","teacher","admin"])
def student(request):
    return render(request, "student.html")

@allowed_users(allowed_roles=["teacher","admin"])
def teacher(request):
    return render(request, "teacher.html")

@allowed_users(allowed_roles=["admin"])
def admin(request):
    return render(request, "admin.html")

class RegisterView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if token:
            try:
                payload = jwt.decode(token, "SECRET_KEY", algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return render(request, "signup.html")

            if User.objects.filter(id = payload['id']).first():
                return redirect("user") #User already logged in

        return render(request, "signup.html")

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        # valid = serializer.is_valid()
        # if not valid:
        #     return render(
        #         request,
        #         "invalid.html",
        #         {
        #             "status" : f"{valid}",
        #             "redirect_url" : "login",
        #             "redirect_to" : "Login",
        #         }
        #     )
        # serializer.save()
        # return Response(serializer.data)

        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as error:
            err = {
                "email": "Email is already Registered. Please Log In.",
                "password": "Password does not meet up with the expectations. Please try again.",
                "username" : "Please enter a unique username."
            }
            e = str(error)
            return render(
                request,
                "invalid.html",
                {
                    "message" : (' '.join(err.get(x,'') for x in err.keys() if x in e)).strip() or e,
                    "redirect_url" : "login",
                    "redirect_to" : "Login",
                }
            )
        

        return render(
            request,
            "signin.html",
            {
                "status": "success",
                "message":"Registration was successful, please Log In with your new details."
            }
        )


class LoginView(APIView):
    def get(self, request):
        token = request.COOKIES.get("jwt")
        if token:
            try:
                payload = jwt.decode(token, "SECRET_KEY", algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                return render(request, "signin.html")

            if User.objects.filter(id = payload['id']).first():
                return redirect("user") #User already logged in

        return render(request, "signin.html")

    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            # raise AuthenticationFailed("User Not Found") #For returning APIs
            return render(
                request,
                "invalid.html",
                {
                    "message" : "Email not found. Please Register.",
                    "redirect_url" : "register",
                    "redirect_to" : "Register",
                }
            )

        
        if not user.check_password(password):
            # raise AuthenticationFailed("Incorrect Password") #For returning APIs
            return render(
                request,
                "invalid.html",
                {
                    "message" : "Incorrect Password. Please Check Your Password and Try Again.",
                    "redirect_url" : "signup",
                    "redirect_to" : "Register",
                }
            )
        
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, "SECRET_KEY", algorithm='HS256')
        # token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')
        response = redirect("user")

        response.set_cookie(key="jwt", value=token, httponly=True)
        
        response.data = {
            "jwt" : token,
        }
        
        return response

class UserView(APIView):
    
    def get(self, request):
        
        token = request.COOKIES.get("jwt")
        
        if not token:
            # raise AuthenticationFailed("Unauthenticated. Please log into your account and enable cookies.")
            response = redirect("home")
            response.data = {
                "status" : status.HTTP_401_UNAUTHORIZED,
                "message" : "You are not logged in. Please login to continue."
            }
            return response
        
        try:
            payload = jwt.decode(token, "SECRET_KEY", algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            response = Response()
            response.delete_cookie(key="jwt")
            response.data = {
                "status" : status.HTTP_403_FORBIDDEN,
                "message":"Logged Out Due To Inactivity",
            }
            # raise AuthenticationFailed("Session Timed Out. Please Log In Again.",token)
            return response

        user = User.objects.filter(id = payload['id']).first()

        serializer = UserSerializer(user)

        return Response(serializer.data)



class LogOutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie(key="jwt")
        response.data = {
            "message":"LogOut Success",
        }
        return response


class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = PasswordResetRequestByEmailSerializer
    def get(self, request):
        return render(request, "forgot_password.html")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        email = request.data['email']

        if User.objects.filter(email = email).exists():
            user = User.objects.get(email = email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            current_site = get_current_site(request= request).domain
            relativeLink = reverse('password-reset', kwargs={'uidb64': uidb64, "token":token})
            absurl = 'http://'+ current_site+ relativeLink
            # import pdb;pdb.set_trace()
            email_body = "Hello " +user.username+ ", Use this link to reset your password \n\n" + absurl
            data = {
                "email_body":email_body,
                "to_email":user.email,
                "email_subject": 'Reset your password',
            }
            Util.send_email(data)
            
            response = redirect("reset_password.html")
            response.data = {
                "status":'Success',
                "message" : "We have sent you a password reset email."
            }
            return response
        elif  not User.objects.filter(email = email).exists():
            response = redirect("home.html")
            response.data = {
                "status" : status.HTTP_403_FORBIDDEN,
                "message" : "User not found. Please Register."
            }
            return response
        else:
            response = redirect("home.html")
            response.data = {
                "status" : status.HTTP_403_FORBIDDEN,
                "message" : "Unknown Error. Please try again."
            }
            return response

class PasswordTokenCheckAPI(APIView):
    pass
