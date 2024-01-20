# Generated by Django 4.2.7 on 2024-01-19 11:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_alter_wallet_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0ca8f229-d1e2-4dfe-9e26-a1de474ad5c1'), editable=False, primary_key=True, serialize=False),
        ),
    ]
