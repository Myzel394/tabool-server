# Generated by Django 3.1.7 on 2021-03-12 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_sessions', '0001_initial'),
        ('sessions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionrelation',
            name='session',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user_sessions.session'),
        ),
    ]
