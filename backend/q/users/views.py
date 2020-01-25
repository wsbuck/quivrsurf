from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseRedirect

from .models import User
from .serializers import UserSerializer, UserSerializerWithToken


class UserCreate(APIView):
    def post(self, request, format=None):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

def activate(request, pk, token):
    user = get_object_or_404(User, pk=pk)
    if user.check_token(token):
        # This is where you could add permissions after a user is activated
        # TODO
        user.active = True
        user.save()
        return HttpResponseRedirect('http://books.williambuck.dev')

    return HttpResponseRedirect('http://books.williambuck.dev')
