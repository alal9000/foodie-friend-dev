# Generated by Django 4.1.5 on 2024-05-04 06:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0009_foodie'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Foodie',
            new_name='Profile',
        ),
        migrations.AddField(
            model_name='event',
            name='attendees',
            field=models.ManyToManyField(blank=True, related_name='attended_events', to='app.profile'),
        ),
    ]