# Generated by Django 4.0.10 on 2023-05-24 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_student_university'),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.student'),
        ),
    ]