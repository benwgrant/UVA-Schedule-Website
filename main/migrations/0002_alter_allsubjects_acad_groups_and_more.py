# Generated by Django 4.1.7 on 2023-03-23 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='allsubjects',
            name='acad_groups',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='campuses',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='careers',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='descr',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='subject',
            field=models.CharField(max_length=50),
        ),
    ]
