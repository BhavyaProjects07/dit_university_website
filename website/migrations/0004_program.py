# Generated by Django 5.1.4 on 2025-03-11 20:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0003_remove_department_department_remove_department_extra_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('duration', models.CharField(max_length=100)),
                ('level', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('syllabus', models.TextField(blank=True, null=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='programs', to='website.department')),
            ],
        ),
    ]
