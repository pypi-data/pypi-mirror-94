from django.conf import settings
from django.contrib.sessions.models import Session
from django.db import models


class UserSessions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_sessions', on_delete=models.CASCADE)
    session = models.OneToOneField(Session, related_name='user_sessions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_sessions'

    def __str__(self):
        return '%s - %s' % (self.user, self.session.session_key)
