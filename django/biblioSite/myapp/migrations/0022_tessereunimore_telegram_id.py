# Generated by Django 4.0.4 on 2022-05-24 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0021_tessereunimore_rewards_lastmodified'),
    ]

    operations = [
        migrations.AddField(
            model_name='tessereunimore',
            name='telegram_id',
            field=models.TextField(null=True, verbose_name='username Telegram'),
        ),
    ]
