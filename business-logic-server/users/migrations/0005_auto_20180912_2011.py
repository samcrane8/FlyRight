# Generated by Django 2.1.1 on 2018-09-12 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_icarususer_picture_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icarususer',
            name='email',
            field=models.TextField(unique=True),
        ),
        migrations.AlterField(
            model_name='icarususer',
            name='username',
            field=models.TextField(unique=True),
        ),
    ]
