# Generated by Django 5.1.6 on 2025-03-03 15:49

import django.db.models.deletion
import django_resized.forms
import users.validators
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view_name', models.CharField(max_length=255, verbose_name='Ko‘rish klassi')),
                ('path_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='URL nomi')),
                ('method', models.CharField(default='post', max_length=255, verbose_name='Usul')),
            ],
            options={
                'verbose_name': 'Ko‘rish oynasi',
                'verbose_name_plural': 'Ko‘rish oynalari',
                'ordering': ['view_name'],
            },
        ),
        migrations.CreateModel(
            name='ViewPermissionRuleCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Nom')),
                ('position', models.SmallIntegerField(default=30, verbose_name='Pozitsiya')),
            ],
            options={
                'verbose_name': 'Ruxsatlar kategoriyasi',
                'verbose_name_plural': 'Ruxsatlar kategoriyalari',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=255, verbose_name='Ism')),
                ('last_name', models.CharField(blank=True, max_length=255, verbose_name='Familiya')),
                ('avatar', django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[400, 400], upload_to='user_avatars/', verbose_name='Rasm')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='Pochta')),
                ('username', models.CharField(max_length=255, unique=True, verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Xodimlarning holati')),
                ('is_active', models.BooleanField(default=True, verbose_name='Faol')),
                ('birthday', models.DateField(blank=True, null=True, verbose_name='Tug‘ilgan kun')),
                ('phone', models.CharField(max_length=255, null=True, validators=[users.validators.phone_validator], verbose_name='Telefon raqami')),
                ('user_type', models.CharField(choices=[('admin', 'Admin'), ('teacher', 'O‘qituvchi'), ('student', 'O‘quvchi')], default='student', max_length=255, verbose_name='Foydalanuvchi turi')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi',
                'verbose_name_plural': 'Foydalanuvchilar',
            },
        ),
        migrations.CreateModel(
            name='ViewPermissionRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Nom')),
                ('position', models.SmallIntegerField(default=30, verbose_name='Pozitsiya')),
                ('permission', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='permission_rule', to='users.viewpermission', verbose_name='Ko‘rish oynasi')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='permission_rule', to='users.viewpermissionrulecategory', verbose_name='Kategoriya')),
            ],
            options={
                'verbose_name': 'Ruxsat',
                'verbose_name_plural': 'Ruxsatlar',
            },
        ),
        migrations.CreateModel(
            name='ViewPermissionRuleGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Nom')),
                ('permissions', models.ManyToManyField(to='users.viewpermissionrule', verbose_name='Ruxsatlar')),
            ],
            options={
                'verbose_name': 'Ruxsatlar guruhi',
                'verbose_name_plural': 'Ruxsatlar guruhlari',
            },
        ),
        migrations.CreateModel(
            name='ViewPermissionRuleGroupToUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users', to='users.viewpermissionrulegroup', verbose_name='Ruxsat guruhi')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permission_groups', to=settings.AUTH_USER_MODEL, verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi guruhi',
                'verbose_name_plural': 'Foydalanuvchi guruhlari',
            },
        ),
        migrations.CreateModel(
            name='ViewPermissionRuleToUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permission', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='users', to='users.viewpermissionrule', verbose_name='Ruxsat')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permissions', to=settings.AUTH_USER_MODEL, verbose_name='Foydalanuvchi')),
            ],
            options={
                'verbose_name': 'Foydalanuvchi ruxsati',
                'verbose_name_plural': 'Foydalanuvchi ruxsatlari',
            },
        ),
    ]
