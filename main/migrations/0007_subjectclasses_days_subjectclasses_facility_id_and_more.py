# Generated by Django 4.1.7 on 2023-03-24 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_alter_subjectclasses_acad_group_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectclasses',
            name='days',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subjectclasses',
            name='facility_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subjectclasses',
            name='instructor',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subjectclasses',
            name='page',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='subjectclasses',
            name='room',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='acad_groups',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='campuses',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='careers',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='descr',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='allsubjects',
            name='subject',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='subjectclasses',
            name='end_time',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='subjectclasses',
            name='start_time',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
