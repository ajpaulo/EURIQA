# Generated by Django 4.0 on 2022-02-15 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0004_auto_20211129_2317'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='max_plugs',
            field=models.IntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='administrator',
            name='picture',
            field=models.ImageField(default='missing_profile.jpg', upload_to='profilephotos/'),
        ),
    ]
