from django.urls import path
from .views import (
    home, 
    student,
    teacher,
    admin,
    RegisterView, 
    LoginView, 
    UserView, 
    LogOutView, 
    RequestPasswordReset, 
    PasswordTokenCheckAPI,
)

urlpatterns = [
    path("", home, name="home"),
    path("home", home, name='home'),
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("user", UserView.as_view(), name="user"),
    path("student", student, name="student"),
    path("teacher", teacher, name="teacher"),
    path("admin", admin, name="admin"),
    path("logout", LogOutView.as_view(), name="logout"),
    path("request-reset-password", RequestPasswordReset.as_view(), name="request-reset-password"),
    path("password-reset/<uidb64>/<token>/", PasswordTokenCheckAPI.as_view(), name="password-reset")
]