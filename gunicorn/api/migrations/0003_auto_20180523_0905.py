# Generated by Django 2.0.5 on 2018-05-23 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.CharField(default=None, max_length=128),
        ),
    ]
