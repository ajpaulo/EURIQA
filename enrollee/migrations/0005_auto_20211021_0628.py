# Generated by Django 3.1.7 on 2021-10-20 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollee', '0004_auto_20210808_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='enrollee',
            name='exam_status',
            field=models.CharField(default='not done', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='enrollee',
            name='program',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='enrollee',
            name='strand',
            field=models.CharField(default='-', max_length=50, null=True),
        ),
    ]
