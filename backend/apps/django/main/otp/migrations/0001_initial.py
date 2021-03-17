# Generated by Django 3.1.7 on 2021-03-12 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_lifecycle.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='IPGeolocation',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='Ip-Adresse')),
                ('longitude', models.PositiveSmallIntegerField()),
                ('latitude', models.PositiveSmallIntegerField()),
                ('city', models.CharField(blank=True, max_length=511, null=True, verbose_name='Stadt')),
            ],
            options={
                'verbose_name': 'IP-Standort',
                'verbose_name_plural': 'IP-Standorte',
                'ordering': ('city', 'ip_address'),
            },
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('token', models.CharField(max_length=6, verbose_name='Token')),
                ('expire_date', models.DateTimeField(verbose_name='Ablaufdatum')),
                ('associated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name': 'Einmalpasswort',
                'verbose_name_plural': 'Einmalpasswörter',
                'ordering': ('expire_date',),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
    ]