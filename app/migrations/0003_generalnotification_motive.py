# Generated by Django 2.2.12 on 2022-05-19 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_generalnotification'),
    ]

    operations = [
        migrations.AddField(
            model_name='generalnotification',
            name='motive',
            field=models.CharField(default='Feedback', max_length=100),
        ),
    ]
