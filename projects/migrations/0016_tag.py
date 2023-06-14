# Generated by Django 4.0.10 on 2023-06-14 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0015_alter_job_cover'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(max_length=50, unique=True)),
                ('job', models.ManyToManyField(to='projects.job')),
                ('project', models.ManyToManyField(to='projects.project')),
            ],
        ),
    ]
