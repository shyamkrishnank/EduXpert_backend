# Generated by Django 4.2.7 on 2024-01-11 04:50

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='id',
            field=models.UUIDField(default=uuid.UUID('0475d518-efa0-421d-8442-e9b30e003992'), editable=False, primary_key=True, serialize=False),
        ),
    ]
