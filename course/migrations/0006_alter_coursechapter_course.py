# Generated by Django 4.2.7 on 2023-12-02 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0005_alter_course_course_category_alter_course_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursechapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='course.course'),
        ),
    ]
