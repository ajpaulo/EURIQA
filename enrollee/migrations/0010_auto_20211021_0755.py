# Generated by Django 3.1.7 on 2021-10-20 23:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrollee', '0009_auto_20211021_0755'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrollee',
            name='strand',
        ),
        migrations.DeleteModel(
            name='Strand',
        ),
    ]