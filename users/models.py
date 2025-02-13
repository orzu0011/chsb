from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django_resized import ResizedImageField
from users.validators import phone_validator


class MyUserManager(BaseUserManager):
    """
    Custom User Manager for handling users with emails as unique identifiers
    """

    def create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user

    def _create_user(self, username, password=None, **extra_fields):
        user = self.model(username=username, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(username, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE = (
        ('admin', 'Admin'),
        ('teacher', 'O‘qituvchi'),
        ('student', 'O‘quvchi'),
    )
    first_name = models.CharField(verbose_name='Ism', max_length=255, blank=True)
    last_name = models.CharField(verbose_name='Familiya', max_length=255, blank=True)
    avatar = ResizedImageField(verbose_name='Rasm',
                                size=[400, 400],
                                crop=['middle', 'center'],
                                null=True, blank=True,
                                upload_to='user_avatars/')
    email = models.EmailField(verbose_name='Pochta', unique=False, blank=True)
    username = models.CharField(verbose_name='username', max_length=255, unique=True)
    is_staff = models.BooleanField(verbose_name='Xodimlarning holati', default=False)
    is_active = models.BooleanField(verbose_name='Faol', default=True)
    birthday = models.DateField(verbose_name="Tug‘ilgan kun",
                                null=True, blank=True)
    phone = models.CharField(verbose_name='Telefon raqami', max_length=255, null=True, blank=False, validators=[phone_validator,])
    user_type = models.CharField(verbose_name='Foydalanuvchi turi', max_length=255, choices=USER_TYPE, default='student')

    USERNAME_FIELD = 'username'
    objects = MyUserManager()

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'
