# Generated by Django 3.0.14 on 2022-05-02 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuition', '0005_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default.jpeg', upload_to='tuition/images'),
        ),
    ]
