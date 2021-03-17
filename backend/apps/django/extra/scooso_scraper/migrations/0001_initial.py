# Generated by Django 3.1.7 on 2021-03-17 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScoosoRequest',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False, help_text='Date and time when this was created', max_length=127, verbose_name='Creation date')),
                ('response', models.CharField(max_length=32767)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
