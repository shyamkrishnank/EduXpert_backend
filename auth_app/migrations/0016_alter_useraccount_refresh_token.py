# Generated by Django 4.2.7 on 2023-12-25 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0015_useraccount_refresh_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='refresh_token',
            field=models.CharField(default=None, max_length=300, null=True),
        ),
    ]
