# Generated by Django 2.1 on 2018-08-23 00:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_icarususer_role'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='icarususer',
            options={},
        ),
        migrations.AlterModelTable(
            name='icarususer',
            table='auth_user',
        ),
    ]
