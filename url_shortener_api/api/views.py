from django.shortcuts import render, redirect
from rest_framework.generics import ListAPIView, CreateAPIView
from django.views import View
from .models import Link
from .serializers import LinkSerializer
from django.conf import settings

class ShortenerListAPIView(ListAPIView):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class ShortenerCreateAPIView(CreateAPIView):
    serializer_class = LinkSerializer

class Redirector(View):
    def get(self, request, shortener_link, *args, **kwargs):
        shortener_link = settings.HOST_URL + "/" + self.kwargs.get("shortener_link")
        redirect_link = Link.objects.filter(shortened_link= shortener_link).first().original_link
        return redirect(redirect_link)