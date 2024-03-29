# Generated by Django 3.1.7 on 2021-03-12 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
        ('course', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubjectrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer'),
        ),
        migrations.AddField(
            model_name='course',
            name='participants',
            field=models.ManyToManyField(to='user.Student', verbose_name='Teilnehmer'),
        ),
        migrations.AddField(
            model_name='course',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.room', verbose_name='Raum'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.subject', verbose_name='Fach'),
        ),
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.teacher', verbose_name='Lehrer'),
        ),
        migrations.AlterUniqueTogether(
            name='usersubjectrelation',
            unique_together={('subject', 'user')},
        ),
    ]
