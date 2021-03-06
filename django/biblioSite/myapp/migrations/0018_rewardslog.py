# Generated by Django 4.0.4 on 2022-05-24 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_delete_rewardslog'),
    ]

    operations = [
        migrations.CreateModel(
            name='RewardsLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_user', models.TextField(verbose_name='codice utente')),
                ('date', models.TextField(verbose_name='data della suggestion')),
                ('suggestion', models.TextField(verbose_name='suggestion')),
            ],
            options={
                'db_table': 'rewards_log',
            },
        ),
    ]
