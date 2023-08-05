import json

import iso8601
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from cryptography.fernet import Fernet
from remo_app.remo.models import Key

User = get_user_model()


def count_active_users() -> int:
    """
    We don't count admin user
    :return: int
    """
    return User.objects.filter(is_active=True, is_superuser=False).count()


class RemoLicense:
    free_tier = 'free'
    premium_tier = 'premium'

    def __init__(self, data: dict):
        self.valid = False
        self.tier = self.free_tier
        self.n_users = 1
        self.expiry = None
        self.lifetime = False

        if data and isinstance(data, dict):
            self.valid = data.get('valid', self.valid)
            self.tier = data.get('tier', self.tier)
            self.n_users = data.get('n_users', self.n_users)
            self.expiry = self.parse_timestamp(data.get('expiry', self.expiry))
            self.lifetime = data.get('lifetime', self.lifetime)

    @staticmethod
    def parse_timestamp(s: str):
        if not s:
            return None
        return iso8601.parse_date(s)

    def is_valid(self) -> bool:
        if not self.is_premium_tier():
            return self.valid
        return self.valid and not self.is_expired()

    def is_expired(self) -> bool:
        if self.lifetime:
            return False

        if not self.expiry:
            return True

        return timezone.now() > self.expiry

    def expires_in_days(self) -> int:
        if self.lifetime:
            return -1

        if self.is_expired():
            return 0

        diff = self.expiry - timezone.now()
        return diff.days

    def is_premium_tier(self) -> bool:
        return self.tier == self.premium_tier

    def to_dict(self):
        return {
            'valid': self.valid,
            'tier': self.tier,
            'n_users': self.n_users,
            'expiry': self.expiry,
            'lifetime': self.lifetime,
            'is_expired': self.is_expired(),
            'expires_in_days': self.expires_in_days(),
            'active_users': count_active_users()
        }


class InvalidRemoLicense(RemoLicense):
    def __init__(self):
        super().__init__({})


class Token(models.Model):
    token = models.CharField(max_length=250)
    license = models.TextField(blank=True, null=True, default='')

    class Meta:
        db_table = 'tokens'

    def save(self, **kwargs):
        if self.license and '{' in self.license:
            cipher = self.get_cipher()
            enc_license = cipher.encrypt(self.license.encode())
            self.license = enc_license.decode()
        super().save(**kwargs)

    def get_cipher(self) -> Fernet:
        db_key = Key.objects.first()
        if db_key:
            key = db_key.key.encode()
        else:
            key = Fernet.generate_key()
            Key.objects.create(key=key.decode())
        return Fernet(key)

    def get_license(self) -> RemoLicense:
        if not self.license:
            return RemoLicense({})

        if '{' in self.license:
            self.save()

        return RemoLicense(
            json.loads(self.get_cipher().decrypt(self.license.encode()).decode())
        )

