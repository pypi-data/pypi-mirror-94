import re
import unicodedata
from datetime import datetime
import warnings

from django.apps import AppConfig
from django.conf import settings
from django.contrib.auth import get_user_model


def validate_password(password: str) -> str:
    if not password:
        return 'adminpass'
    return password


def normalize_user_info(email: str, username: str, fullname: str):
    first_name, last_name = split_fullname(fullname)

    username = normalize_username(username)
    if not username:
        username = normalize_username(first_name)
    if not username:
        username = normalize_username(email.split('@', 1)[0])
    if not username:
        username = 'remo'

    if not email:
        email = f'{username}@remo.ai'

    email = email.lower()
    return email, username, first_name, last_name


def normalize_username(username: str) -> str:
    if isinstance(username, str):
        username = re.sub(r"[\s-]+", "_", username.lower())
        username = re.sub(r"[^.\w\d_]+", "", username)
        return unicodedata.normalize('NFKC', username)
    return ''


def split_fullname(fullname: str) -> (str, str):
    first_name, last_name = '', ''
    fullname = fullname.strip().split(' ', 1)
    if len(fullname) == 2:
        first_name, last_name = fullname
    else:
        first_name = fullname[0]
    return first_name, last_name


class RemoConfig(AppConfig):
    name = 'remo_app.remo'

    def ready(self):
        from remo_app.remo.signals import signals  # noqa
        self.set_remo_license()
        self.create_remo_admin()

    @staticmethod
    def create_remo_admin():
        try:
            password = validate_password(settings.REMO_ADMIN_PASS)
            email, username, first_name, last_name = normalize_user_info(settings.REMO_ADMIN_EMAIL,
                                                                         settings.REMO_ADMIN_USERNAME,
                                                                         settings.REMO_ADMIN_FULLNAME)
            User = get_user_model()
            user = User.objects.filter(is_superuser=True).first()
            warnings.simplefilter("ignore")
            if not user:
                user = User.objects.create_superuser(username, email, password, last_login=datetime.now())
            else:
                user.email = email
                user.username = username
                user.set_password(password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except Exception:
            pass

    @staticmethod
    def set_remo_license():
        try:
            from remo_app.remo.services.license import is_valid_token
            if settings.REMO_TOKEN:
                is_valid_token(settings.REMO_TOKEN)
        except Exception:
            pass
