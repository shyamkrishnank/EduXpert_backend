# Generated by Django 4.2.7 on 2024-01-20 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0016_reviewrepley_timestamp_alter_reviewlikes_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewlikes',
            name='is_liked',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='reviewlikes',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='course.reviews'),
        ),
        migrations.AlterField(
            model_name='reviewrepley',
            name='review',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply', to='course.reviews'),
        ),
    ]
