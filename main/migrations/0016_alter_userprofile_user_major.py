# Generated by Django 4.1.7 on 2023-04-14 01:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_advisorprofile_instructor_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='user_major',
            field=models.CharField(default='N/C', max_length=255),
        ),
    ]
