# Generated by Django 4.0.10 on 2023-05-24 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_alter_job_student'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='job_begin',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_end',
            field=models.DateField(),
        ),
    ]
