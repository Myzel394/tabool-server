# Generated by Django 3.1.7 on 2021-03-12 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('timetable', '0001_initial'),
        ('homework', '0001_initial'),
        ('user', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userhomeworkrelation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer'),
        ),
        migrations.AddField(
            model_name='submission',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.lesson', verbose_name='Stunde'),
        ),
        migrations.AddField(
            model_name='submission',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.student', verbose_name='Schüler'),
        ),
        migrations.AddField(
            model_name='material',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.lesson', verbose_name='Stunde'),
        ),
        migrations.AddField(
            model_name='homework',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.lesson', verbose_name='Stunde'),
        ),
        migrations.AddField(
            model_name='homework',
            name='private_to_student',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='user.student', verbose_name='Schüler'),
        ),
        migrations.AddField(
            model_name='classbook',
            name='lesson',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timetable.lesson', verbose_name='Stunde'),
        ),
        migrations.AlterUniqueTogether(
            name='userhomeworkrelation',
            unique_together={('homework', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='classbook',
            unique_together={('lesson', 'lesson_date')},
        ),
    ]
