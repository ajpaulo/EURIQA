# Generated by Django 4.0 on 2022-02-15 18:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('administrator', '0005_exam_max_plugs_alter_administrator_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='exam',
            old_name='max_plugs',
            new_name='max_flags',
        ),
    ]