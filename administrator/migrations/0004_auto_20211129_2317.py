# Generated by Django 3.1.7 on 2021-11-29 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0003_auto_20211129_2317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrator',
            name='picture',
            field=models.ImageField(default='missing_profile.jpg', upload_to='static/profilephotos/'),
        ),
    ]