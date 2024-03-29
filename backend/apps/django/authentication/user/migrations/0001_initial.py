# Generated by Django 3.1.7 on 2021-03-12 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_lifecycle.mixins
import simple_email_confirmation.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('id', models.CharField(blank=True, editable=False, max_length=19, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email-Adresse')),
                ('gender', models.CharField(choices=[('MALE', 'Männlich'), ('FEMALE', 'Weiblich'), ('DIVERSE', 'Divers')], default='DIVERSE', max_length=7, verbose_name='Geschlecht')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'permissions': (('change_user_permissions', 'Kann Benutzer-Berechtigungen verändern'),),
            },
            bases=(simple_email_confirmation.models.SimpleEmailConfirmationUserMixin, django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('short_name', models.CharField(max_length=32, verbose_name='Initialien')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name': 'Lehrer',
                'verbose_name_plural': 'Lehrer',
                'ordering': ('user',),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('class_number', models.PositiveSmallIntegerField(choices=[(5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13)], verbose_name='Klassenstufe')),
                ('main_teacher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.teacher', verbose_name='Lehrer')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name': 'Schüler',
                'verbose_name_plural': 'Schüler',
                'ordering': ('user', 'class_number'),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Preference',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('data', models.TextField(default='{}', max_length=16383)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Präferenz',
                'verbose_name_plural': 'Präferenzen',
                'ordering': ('user',),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='KnownIp',
            fields=[
                ('id', models.CharField(max_length=8, primary_key=True, serialize=False, unique=True)),
                ('expire_date', models.DateTimeField(verbose_name='Ablaufdatum')),
                ('ip_address', models.GenericIPAddressField(verbose_name='Ip-Adresse')),
                ('associated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name': 'Bekannte IP',
                'verbose_name_plural': 'Bekannte Ips',
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]
