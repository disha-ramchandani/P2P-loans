# Generated by Django 4.1.3 on 2023-04-11 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_rename_default_on_file_profile_cb_person_default_on_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='liquid_funds',
            field=models.FloatField(default=0),
        ),
    ]
