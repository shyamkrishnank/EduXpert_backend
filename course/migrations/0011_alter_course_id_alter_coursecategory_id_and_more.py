# Generated by Django 4.2.7 on 2023-12-25 05:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_alter_course_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='coursecategory',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='coursechapter',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
