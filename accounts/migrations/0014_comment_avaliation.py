# Generated by Django 4.0.10 on 2023-05-27 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='avaliation',
            field=models.IntegerField(default=0),
        ),
    ]
