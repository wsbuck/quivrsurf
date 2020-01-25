from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.signing import TimestampSigner, BadSignature, SignatureExpired
from django.urls import reverse

from datetime import timedelta

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField('email_address', unique=True)
    first_name = models.CharField('fist name', max_length=30, blank=False)
    last_name = models.CharField('last name', max_length=30, blank=False)
    date_joined = models.DateTimeField('date joined', auto_now_add=True)
    active = models.BooleanField('active', default=False)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
    
    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)
    
    def create_activation_link(self):
        pk, token = self.make_token().split(":", 1)
        return reverse('activate', kwargs={'pk': pk, 'token': token})
    
    def make_token(self):
        return TimestampSigner().sign(self.pk)
    
    def check_token(self, token):
        try:
            key = "{}:{}".format(self.pk, token)
            TimestampSigner().unsign(key, max_age=timedelta(hours=24 * 10))
        except (BadSignature, SignatureExpired):
            return False
        return True
