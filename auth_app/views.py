from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView


class AuthenticatedView(APIView):
    pass


class UnauthenticatedView(APIView):
    permission_classes = ()