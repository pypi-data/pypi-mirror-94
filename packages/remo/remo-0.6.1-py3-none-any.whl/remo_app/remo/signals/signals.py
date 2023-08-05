from django.contrib.auth.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.dispatch import receiver
from remo_app.remo.models import UserSessions


@receiver(user_logged_in)
def concurrent_logins(sender, **kwargs):
    user = kwargs.get('user')
    request = kwargs.get('request')

    if user is not None and request is not None:
        session = Session.objects.get(session_key=request.session.session_key)

        try:
            if not UserSessions.objects.filter(session=session).exists():
                UserSessions.objects.create(user=user, session=session)
        except Exception:
            pass

        if user.user_sessions.count() > 1:
            for user_session in UserSessions.objects.filter(user=user).exclude(session=session):
                user_session.session.delete()
