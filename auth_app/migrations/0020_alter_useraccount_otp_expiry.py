# Generated by Django 4.2.7 on 2024-01-17 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0019_useraccount_otp_expiry'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='otp_expiry',
            field=models.DateTimeField(null=True),
        ),
    ]
