# Generated by Django 3.0.14 on 2022-07-03 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_auto_20220701_1225'),
    ]

    operations = [
        migrations.AddField(
            model_name='tuitionprofile',
            name='current_status',
            field=models.CharField(choices=[('Graduated/Passed', 'Graduated/Passed'), ('Studying', 'Studying')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='tuitionprofile',
            name='id_certificate',
            field=models.ImageField(blank=True, upload_to='session/id_certificate/'),
        ),
        migrations.AlterField(
            model_name='tuitionprofile',
            name='major_subject',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
