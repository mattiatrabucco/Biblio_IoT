# Generated by Django 4.0.4 on 2022-05-24 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_alter_rewardslog_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RewardsLog',
        ),
    ]
