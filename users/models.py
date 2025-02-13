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


class ViewPermission(models.Model):
    view_name = models.CharField(verbose_name='Ko‘rish klassi', max_length=255)
    path_name = models.CharField(verbose_name='URL nomi', max_length=255, null=True, blank=True)
    method = models.CharField(verbose_name='Usul', max_length=255, default='post')

    class Meta:
        verbose_name = 'Ko‘rish oynasi'
        verbose_name_plural = 'Ko‘rish oynalari'
        ordering = ['view_name']

    def __str__(self):
        return f'{self.path_name} - {self.view_name} - {self.method}'


class ViewPermissionRule(models.Model):
    title = models.CharField(verbose_name='Nom', max_length=255)
    permission = models.OneToOneField('ViewPermission', verbose_name='Ko‘rish oynasi',
                                      on_delete=models.PROTECT, related_name='permission_rule')
    category = models.ForeignKey('ViewPermissionRuleCategory', verbose_name='Kategoriya',
                                 on_delete=models.PROTECT, related_name='permission_rule',
                                 null=True, blank=True)
    position = models.SmallIntegerField(verbose_name='Pozitsiya', default=30)

    class Meta:
        verbose_name = 'Ruxsat'
        verbose_name_plural = 'Ruxsatlar'

    def __str__(self):
        return self.title


class ViewPermissionRuleCategory(models.Model):
    title = models.CharField(verbose_name='Nom', max_length=255)
    position = models.SmallIntegerField(verbose_name='Pozitsiya', default=30)

    class Meta:
        verbose_name = 'Ruxsatlar kategoriyasi'
        verbose_name_plural = 'Ruxsatlar kategoriyalari'

    def __str__(self):
        return self.title


class ViewPermissionRuleGroup(models.Model):
    title = models.CharField(verbose_name='Nom', max_length=255)
    permissions = models.ManyToManyField('ViewPermissionRule', verbose_name='Ruxsatlar')

    class Meta:
        verbose_name = 'Ruxsatlar guruhi'
        verbose_name_plural = 'Ruxsatlar guruhlari'

    def __str__(self):
        return self.title


class ViewPermissionRuleToUser(models.Model):
    user = models.ForeignKey('User', verbose_name='Foydalanuvchi',
                             on_delete=models.CASCADE, related_name='permissions')
    permission = models.ForeignKey('ViewPermissionRule', verbose_name='Ruxsat',
                                   on_delete=models.PROTECT, related_name='users')

    class Meta:
        verbose_name = 'Foydalanuvchi ruxsati'
        verbose_name_plural = 'Foydalanuvchi ruxsatlari'


class ViewPermissionRuleGroupToUser(models.Model):
    user = models.ForeignKey('User', verbose_name='Foydalanuvchi',
                             on_delete=models.CASCADE, related_name='permission_groups')
    group = models.ForeignKey('ViewPermissionRuleGroup', verbose_name='Ruxsat guruhi',
                              on_delete=models.PROTECT, related_name='users')

    class Meta:
        verbose_name = 'Foydalanuvchi guruhi'
        verbose_name_plural = 'Foydalanuvchi guruhlari'
