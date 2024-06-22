from auth_app.models import User, UserSession


class AuthDatalayer(object):

    @classmethod
    def create_user(cls, username, email, password):

        if User.objects.filter(username=username).exists():
            raise Exception('Same username already exist')

        user = User(
            username=username,
            email=email
        )
        user.set_password(password)

        user.save()

        return 0

    @classmethod
    def check_active_session_of_user(cls, user):

        if UserSession.objects.filter(user=user, is_active=True).exists():
            return True
        return False
