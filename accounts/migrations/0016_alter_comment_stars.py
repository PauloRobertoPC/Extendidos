# Generated by Django 4.0.10 on 2023-05-27 16:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_rename_avaliation_comment_stars'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='stars',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
