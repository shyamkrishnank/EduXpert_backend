# Generated by Django 4.2.7 on 2024-01-06 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_alter_chat_id_alter_chatroom_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='content',
            field=models.CharField(default='message', max_length=1000),
        ),
    ]