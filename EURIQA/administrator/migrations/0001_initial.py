# Generated by Django 3.1.7 on 2021-11-29 11:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Administrator',
            fields=[
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('middle_name', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=50)),
                ('position', models.CharField(max_length=50)),
                ('picture', models.FileField(null=True, upload_to='static/profilephotos/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'administrator',
            },
        ),
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default=None, max_length=100)),
                ('takers', models.CharField(default=None, max_length=100)),
                ('total_items', models.IntegerField(default=None, null=True)),
                ('overall_points', models.IntegerField(default=None, null=True)),
                ('link', models.CharField(max_length=5000, null=True)),
                ('created_by', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.administrator')),
            ],
            options={
                'db_table': 'exam',
            },
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('part_id', models.AutoField(primary_key=True, serialize=False)),
                ('part_name', models.CharField(max_length=200)),
                ('instructions', models.CharField(max_length=200)),
                ('overall_points', models.IntegerField(default=None, null=True)),
                ('total_items', models.IntegerField(default=None, null=True)),
                ('exam', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.exam')),
            ],
            options={
                'db_table': 'exam_parts',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('question_id', models.AutoField(primary_key=True, serialize=False)),
                ('question_no', models.IntegerField(default=None, null=True)),
                ('question', models.CharField(max_length=200)),
                ('optionA', models.CharField(max_length=100)),
                ('optionB', models.CharField(max_length=100)),
                ('optionC', models.CharField(max_length=100)),
                ('optionD', models.CharField(max_length=100)),
                ('answer', models.CharField(max_length=100)),
                ('points', models.IntegerField(default=None, null=True)),
                ('exam', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.exam')),
                ('part', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='administrator.part')),
            ],
            options={
                'db_table': 'question',
            },
        ),
    ]
