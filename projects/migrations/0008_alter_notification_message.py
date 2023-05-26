# Generated by Django 4.0.10 on 2023-05-26 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_alter_notification_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='message',
            field=models.CharField(choices=[('READ', 'Read'), ('WAITING', 'Waiting')], default='WAITING', max_length=8),
        ),
    ]