# Generated by Django 4.2.7 on 2024-01-17 04:16

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_alter_wallet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='id',
            field=models.UUIDField(default=uuid.UUID('7a6085b2-341d-4b63-b95c-8c1d88072f98'), editable=False, primary_key=True, serialize=False),
        ),
    ]
