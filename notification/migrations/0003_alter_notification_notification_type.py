# Generated by Django 4.2.7 on 2024-01-06 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0002_notification_room'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(default='message', max_length=255),
        ),
    ]
