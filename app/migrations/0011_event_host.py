# Generated by Django 4.1.5 on 2024-05-06 01:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_rename_foodie_profile_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='host',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.profile'),
        ),
    ]