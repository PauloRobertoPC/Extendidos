# Generated by Django 4.0.10 on 2023-06-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0014_job_cover_project_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='cover',
            field=models.ImageField(default='jobs/default_job.jpeg', upload_to='jobs/'),
        ),
    ]