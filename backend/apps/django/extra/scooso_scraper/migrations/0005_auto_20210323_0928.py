# Generated by Django 3.1.7 on 2021-03-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scooso_scraper', '0004_auto_20210321_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='scoosorequest',
            name='attempts_required',
            field=models.PositiveSmallIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='scoosorequest',
            name='request_data',
            field=models.TextField(default='', max_length=131071),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='scoosorequest',
            name='response',
            field=models.TextField(max_length=131071),
        ),
    ]