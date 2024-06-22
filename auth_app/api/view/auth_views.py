from django.contrib.auth import authenticate
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from auth_app.authentication import TokenGeneration
from auth_app.datalayer import AuthDatalayer
from auth_app.models.black_list_token import BlacklistedToken
from auth_app.serializers import TokenSerializer, RefreshTokenSerializer, UserSerializer
from auth_app.views import UnauthenticatedView, AuthenticatedView
from auth_app.models import UserSession
from django.utils import timezone


class IsSuperUser(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser


class RegisterUserApiView(AuthenticatedView):
    permission_classes = (IsSuperUser,)

    def post(self, request):

        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            is_error = AuthDatalayer.create_user(
                username=serializer.validated_data.get('username'),
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password')
            )

            return Response(
                dict(
                    is_error=is_error,
                    message='success'
                ), status=status.HTTP_200_OK
            )

        except Exception as exe:
            return Response(
                dict(
                    status=500,
                    message=str(exe)
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateJwtTokenApiView(UnauthenticatedView):

    def post(self, request):
        try:
            serializer = TokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                access_token = TokenGeneration.generate_access_token(user)
                refresh_token = TokenGeneration.generate_refresh_token(user)

                UserSession.objects.create(user=user, refresh_token=refresh_token)

                data = dict(
                    access=access_token,
                    refresh=refresh_token,
                )
                return Response(
                    data, status=status.HTTP_200_OK
                )

            else:
                return Response(
                    dict(
                        status=401,
                        message='username or password mismatched'
                    ), status=status.HTTP_401_UNAUTHORIZED
                )

        except Exception as exe:
            return Response(
                dict(
                    status=500,
                    message=str(exe)
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RefreshTokenApiView(UnauthenticatedView):
    def post(self, request):
        try:
            serializer = RefreshTokenSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            refresh = serializer.validated_data.get('refresh')
            access_token = TokenGeneration.get_access_token_from_refresh(refresh_token=refresh)
            data = dict(
                access=access_token
            )
            return Response(
                data, status=status.HTTP_200_OK
            )
        except Exception as exe:
            return Response(
                dict(
                    status=500,
                    message=str(exe)
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LogoutView(AuthenticatedView):

    def post(self, request):

        try:
            refresh_token = request.data["refresh"]

            if not refresh_token:
                raise Exception('Invalid refresh token')
            session = UserSession.objects.get(refresh_token=refresh_token)
            session.logout_time = timezone.now()
            session.save()

            BlacklistedToken.objects.create(token=refresh_token)

            logout(request)

            return Response(dict(message="Successfully logged out"), status=status.HTTP_205_RESET_CONTENT)

        except Exception as exe:
            return Response(
                dict(
                    status=500,
                    message=str(exe)
                ), status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
