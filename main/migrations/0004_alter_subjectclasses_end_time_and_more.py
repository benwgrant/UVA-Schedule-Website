# Generated by Django 4.1.7 on 2023-03-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_allsubjects_acad_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subjectclasses',
            name='end_time',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='subjectclasses',
            name='start_time',
            field=models.CharField(max_length=20),
        ),
    ]
