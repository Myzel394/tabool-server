# Generated by Django 3.1.7 on 2021-03-12 19:28

import apps.django.main.homework.public.file_uploads
import apps.django.main.homework.public.validators
import apps.django.utils.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_common_utils.libraries.handlers.models
import django_lifecycle.mixins
import private_storage.fields
import private_storage.storage.files
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lesson', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Homework',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False, help_text='Date and time when this was created', max_length=127, verbose_name='Creation date')),
                ('due_date', models.DateTimeField(blank=True, null=True, validators=[apps.django.utils.validators.validate_weekday_in_lesson_data_available], verbose_name='Fälligkeitsdatum')),
                ('information', models.TextField(blank=True, max_length=8191, null=True, verbose_name='Informationen')),
                ('type', models.CharField(blank=True, help_text='Beispiel: Vortag, Hausaufgabe, Protokoll, Hausarbeit', max_length=127, null=True, verbose_name='Hausaufgaben-Typ')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson', verbose_name='Stunde')),
                ('private_to_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name': 'Hausaufgabe',
                'verbose_name_plural': 'Hausaufgaben',
                'ordering': ('due_date', 'type'),
                'permissions': (('can_view_private_homework', 'Kann private Hausaufgaben sehen und bearbeiten'),),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model, django_common_utils.libraries.handlers.models.HandlerMixin),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('added_at', models.DateTimeField(blank=True, null=True, verbose_name='Hinzugefügt')),
                ('file', private_storage.fields.PrivateFileField(blank=True, max_length=1023, null=True, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=apps.django.main.homework.public.file_uploads.build_material_upload_to, verbose_name='Datei')),
                ('_original_filename', models.CharField(blank=True, max_length=255, null=True, verbose_name='Originaler Dateiname')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Dateiname')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='Gelöscht')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson', verbose_name='Stunde')),
            ],
            options={
                'verbose_name': 'Material',
                'verbose_name_plural': 'Materialien',
                'ordering': ('is_deleted', '-added_at', 'name'),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(editable=False, help_text='Date and time when this was created', max_length=127, verbose_name='Creation date')),
                ('file', private_storage.fields.PrivateFileField(max_length=1023, storage=private_storage.storage.files.PrivateFileSystemStorage(), upload_to=apps.django.main.homework.public.file_uploads.build_submission_upload_to, validators=[apps.django.main.homework.public.validators.safe_file_validator], verbose_name='Datei')),
                ('upload_date', models.DateTimeField(blank=True, help_text='Wann soll die Datei hochgeladen werden?', null=True, verbose_name='Hochladedatum')),
                ('is_uploaded', models.BooleanField(default=False, verbose_name='Hochgeladen?')),
                ('is_in_action', models.BooleanField(default=False, help_text='Wenn ja, dann versucht der Server gerade die Datei hochzuladen.', verbose_name='Wird hochgeladen')),
                ('associated_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lesson.lesson', verbose_name='Stunde')),
            ],
            options={
                'verbose_name': 'Einreichung',
                'verbose_name_plural': 'Einreichungen',
                'ordering': ('lesson', 'upload_date'),
            },
            bases=(django_lifecycle.mixins.LifecycleModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SubmissionScoosoData',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('scooso_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Scooso-ID')),
                ('submission', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='homework.submission', verbose_name='Einreichung')),
            ],
            options={
                'verbose_name': 'Einreichung-Scooso-Daten',
                'verbose_name_plural': 'Einreichung-Scooso-Daten',
                'ordering': ('submission', 'scooso_id'),
            },
        ),
        migrations.CreateModel(
            name='MaterialScoosoData',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('scooso_id', models.PositiveIntegerField(blank=True, null=True, verbose_name='Scooso-ID')),
                ('owner_id', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Besitzer-Scooso-ID')),
                ('material', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='homework.material', verbose_name='Material')),
            ],
            options={
                'verbose_name': 'Material-Scooso-Daten',
                'verbose_name_plural': 'Material-Scooso-Daten',
                'ordering': ('material', 'scooso_id'),
            },
        ),
        migrations.CreateModel(
            name='HistoricalHomework',
            fields=[
                ('id', models.CharField(db_index=True, editable=False, help_text='An unique ID for the object', max_length=127, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP-Adresse')),
                ('due_date', models.DateTimeField(blank=True, null=True, validators=[apps.django.utils.validators.validate_weekday_in_lesson_data_available], verbose_name='Fälligkeitsdatum')),
                ('information', models.TextField(blank=True, max_length=8191, null=True, verbose_name='Informationen')),
                ('type', models.CharField(blank=True, help_text='Beispiel: Vortag, Hausaufgabe, Protokoll, Hausarbeit', max_length=127, null=True, verbose_name='Hausaufgaben-Typ')),
                ('history_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.TextField(null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='lesson.lesson', verbose_name='Stunde')),
            ],
            options={
                'verbose_name': 'historical Hausaufgabe',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='UserHomeworkRelation',
            fields=[
                ('id', models.CharField(editable=False, help_text='An unique ID for the object', max_length=127, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('completed', models.BooleanField(default=False, verbose_name='Erledigt')),
                ('ignore', models.BooleanField(default=False, verbose_name='Ignorieren')),
                ('homework', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='homework.homework', verbose_name='Hausaufgabe')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Benutzer')),
            ],
            options={
                'verbose_name': 'Hausaufgabe-Benutzer-Beziehung',
                'verbose_name_plural': 'Hausaufgabe-Benutzer-Beziehungen',
                'ordering': ('homework', 'user'),
                'unique_together': {('homework', 'user')},
            },
        ),
    ]
