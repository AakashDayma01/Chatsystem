# Generated by Django 5.1.2 on 2025-01-14 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_message_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='Passkey',
            field=models.CharField(blank=True, max_length=15, unique=True),
        ),
        migrations.AddField(
            model_name='room',
            name='Privacy',
            field=models.CharField(choices=[('Private', 'Private'), ('Public', 'Public')], default='Private', max_length=10),
        ),
    ]
