# Generated by Django 3.1.7 on 2021-11-29 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='picture',
            field=models.ImageField(null=True, upload_to='static/profilephotos/'),
        ),
    ]
