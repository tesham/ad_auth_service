import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from user_service import settings
from auth_app.models import User


class SafeJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_header = request.headers.get('Authorization')

        if not authorization_header:
            return None
        try:
            access_token = authorization_header.split(' ')[1]
            private_key = getattr(settings, 'JWT_SECRET_KEY')
            payload = jwt.decode(
                access_token, private_key, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('access_token expired')
        except IndexError:
            raise exceptions.AuthenticationFailed('Token prefix missing')
        except Exception as exe:
            raise exceptions.AuthenticationFailed('Invalid token')

        user = User.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not found')

        return user, None