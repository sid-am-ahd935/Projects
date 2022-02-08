from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage

class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject= data['email_subject'],
            body= data["email_body"],
            to= (data['to_email'],),
        )
        # print(email, 99191919, data)
        email.send()


def allowed_users(allowed_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            print("Working:", allowed_roles)
            print(request.user.groups.all())
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return render(request, "invalid.html", {
                    "message" : "You are not authorised to view this page.",
                    "redirect_url" : "home", 
                    "redirect_to" : "Home",
                    })

            return view_func(request, *args, **kwargs)
        return wrapper_func
    return decorator