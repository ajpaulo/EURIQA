# Generated by Django 4.0 on 2022-02-16 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0006_rename_max_plugs_exam_max_flags'),
    ]

    operations = [
        migrations.AddField(
            model_name='exam',
            name='duration_hr',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='exam',
            name='duration_min',
            field=models.IntegerField(default=0),
        ),
    ]
