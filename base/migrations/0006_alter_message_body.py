# Generated by Django 5.1.2 on 2025-01-13 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_message_audio_message_file_message_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
    ]
