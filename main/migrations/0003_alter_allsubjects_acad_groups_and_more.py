# Generated by Django 4.1.7 on 2023-03-23 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_allsubjects_acad_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allsubjects',
            name='acad_groups',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='campuses',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='careers',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='descr',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='subject',
            field=models.CharField(max_length=200),
        ),
    ]
