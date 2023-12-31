# Generated by Django 4.1.7 on 2023-04-01 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_subjectclasses_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('num_credits', models.IntegerField()),
                ('num_classes', models.IntegerField()),
                ('classes', models.ManyToManyField(to='main.subjectclasses')),
            ],
        ),
    ]
