import datetime

import jwt
from django.utils import timezone

from auth_app.models.black_list_token import BlacklistedToken
from auth_service import settings
from rest_framework import exceptions

from auth_app.models import User, UserSession


class TokenGeneration(object):

    @classmethod
    def generate_access_token(cls, user):

        """
            Generate access token for user
            Expiration time : 2 hours
        """
        user_session = UserSession.objects.filter(user=user, is_active=True).first()
        payload = {
            'iss': 'tesham29@gmail.com',
            'sub': 'access token',
            'user_id': user.id,
            'name': user.username,
            'session_id': user_session.id if user_session else None,
            'role': 'user',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, hours=2, minutes=0),
            'iat': datetime.datetime.utcnow(),
        }
        private_key = getattr(settings, 'JWT_SECRET_KEY')
        access_token = jwt.encode(payload,
                                  private_key, algorithm='HS256') \
            # .decode('utf-8')
        return access_token

    @classmethod
    def generate_refresh_token(cls, user):

        """
            Generate refresh token for user, It is used to generate access token if access token expired
            Expiration time : 1 day
        """

        refresh_token_payload = {
            'iss': 'tesham29@gmail.com',
            'sub': 'refresh token',
            'user_id': user.id,
            'name': user.username,
            'role': 'user',
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=0, minutes=0),
            'iat': datetime.datetime.utcnow(),
        }
        private_key = getattr(settings, 'JWT_SECRET_KEY')
        refresh_token = jwt.encode(
            refresh_token_payload, private_key, algorithm='HS256') \
            # .decode('utf-8')

        return refresh_token

    @classmethod
    def verify_refresh_token(cls, refresh_token):
        # Check if the refresh token is blacklisted
        if BlacklistedToken.objects.filter(token=refresh_token).exists():
            return False
        else:
            return True


    @classmethod
    def get_access_token_from_refresh(cls, refresh_token):

        """
            Generate access token from refresh token
            validation:
             1. Check if refresh token is provided
             2. Checking if the token blacklisted
             3. If refresh token is expired then inactive the user session for that token

            :param  refresh_token
            :return access token
        """

        if refresh_token is None:
            raise exceptions.AuthenticationFailed(
                'Refresh token not provided.')

        #  Check if refresh_token is valid or not used
        if not cls.verify_refresh_token(refresh_token=refresh_token):
            raise Exception('Blacklisted refresh token')

        try:
            private_key = getattr(settings, 'JWT_SECRET_KEY')
            payload = jwt.decode(
                refresh_token, private_key, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            session = UserSession.objects.filter(refresh_token=refresh_token, is_active=True).first()
            if session:
                session.logout_time = timezone.now()
                session.is_active = False
                session.save()
            raise exceptions.AuthenticationFailed(
                'expired refresh token, please login again.')

        user = User.objects.filter(id=payload.get('user_id')).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        access_token = cls.generate_access_token(user)
        return access_token
