# Generated by Django 3.1.7 on 2021-03-12 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('poll', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='associated_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer'),
        ),
        migrations.AddField(
            model_name='vote',
            name='choices',
            field=models.ManyToManyField(to='poll.Choice', verbose_name='Auswahlen'),
        ),
        migrations.AddField(
            model_name='vote',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.poll', verbose_name='Umfrage'),
        ),
        migrations.AddField(
            model_name='poll',
            name='targeted_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Benutzer'),
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='poll.poll'),
        ),
    ]
