# Generated by Django 5.0.7 on 2024-07-21 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fetcher', '0002_rename_chanell_lastmessages_channel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lastmessages',
            name='photo_url',
        ),
        migrations.AddField(
            model_name='lastmessages',
            name='media_url',
            field=models.TextField(blank=True),
        ),
    ]
