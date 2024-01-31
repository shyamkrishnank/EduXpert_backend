# Generated by Django 4.2.7 on 2024-01-17 04:14

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0008_alter_wallet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b03150f0-3616-498b-b6c6-434a96eb55fe'), editable=False, primary_key=True, serialize=False),
        ),
    ]