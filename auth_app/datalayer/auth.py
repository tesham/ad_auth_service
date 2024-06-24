from auth_app.models import User, UserSession
from auth_app.rabbitmq_producer import send_message


class AuthDatalayer(object):

    @classmethod
    def create_user(cls, username, email, password, user=None):

        if User.objects.filter(username=username).exists():
            raise Exception('Same username already exist')

        u = User(
            username=username,
            email=email
        )
        u.set_password(password)

        u.save()

        message = dict(
            user=user.name if user else '',
            session_id=user.session_id if user else '',
            module='AUTH',
            label='Register',
            action=f'user register : {username}'
        )

        send_message("audit_queue", message)

        return 0

    @classmethod
    def check_active_session_of_user(cls, user):

        if UserSession.objects.filter(user=user, is_active=True).exists():
            return True
        return False
