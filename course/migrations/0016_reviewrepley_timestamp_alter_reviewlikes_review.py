# Generated by Django 4.2.7 on 2024-01-19 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0015_alter_reviewlikes_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewrepley',
            name='timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='reviewlikes',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked_count', to='course.reviews'),
        ),
    ]
