# Generated by Django 4.0.4 on 2022-04-26 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_tessereunimore_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tessereunimore',
            name='mail',
            field=models.TextField(),
        ),
    ]
