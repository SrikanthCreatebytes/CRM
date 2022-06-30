from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth import settings
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from .managers import UserManager

USER_ROLE = [
    ('EMPLOYEE', 'employee'),
    ('STUDENT', 'student')
]


class User(AbstractBaseUser, PermissionsMixin):
    """
        User Model
        """
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    role = models.CharField(max_length=100, choices=USER_ROLE, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'


class Enquire(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    course_interest = models.CharField(max_length=100)
    claimed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   default=None, blank=True, null=True, related_name='enquiry')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['pk']