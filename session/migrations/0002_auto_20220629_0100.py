# Generated by Django 3.0.14 on 2022-06-28 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='gender',
        ),
        migrations.AddField(
            model_name='tuitionprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=20, null=True),
        ),
    ]
