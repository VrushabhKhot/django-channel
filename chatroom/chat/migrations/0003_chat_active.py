# Generated by Django 4.1.7 on 2023-03-26 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_chatroom_chat'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]