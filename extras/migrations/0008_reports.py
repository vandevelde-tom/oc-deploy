# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 21:25

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import connection, migrations, models
import django.db.models.deletion
from django.db.utils import OperationalError


def verify_postgresql_version(apps, schema_editor):
    """
    Verify that PostgreSQL is version 9.4 or higher.
    """
    # https://www.postgresql.org/docs/current/libpq-status.html#LIBPQ-PQSERVERVERSION
    DB_MINIMUM_VERSION = 90400  # 9.4.0

    try:
        pg_version = connection.pg_version

        if pg_version < DB_MINIMUM_VERSION:
            raise Exception("PostgreSQL 9.4.0 ({}) or higher is required ({} found). Upgrade PostgreSQL and then run migrations again.".format(DB_MINIMUM_VERSION, pg_version))

    # Skip if the database is missing (e.g. for CI testing) or misconfigured.
    except OperationalError:
        pass


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('extras', '0007_unicode_literals'),
    ]

    operations = [
        migrations.RunPython(verify_postgresql_version),
        migrations.CreateModel(
            name='ReportResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.CharField(max_length=255, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('failed', models.BooleanField()),
                ('data', django.contrib.postgres.fields.jsonb.JSONField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['report'],
            },
        ),
    ]
