# Generated by Django 2.0.4 on 2018-04-28 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('picture', models.CharField(max_length=128, unique=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('bio', models.CharField(max_length=128)),
                ('karma', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]