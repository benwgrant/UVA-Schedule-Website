from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('main', '0021_alter_schedule_options'),
    ]

    operations = [
        TrigramExtension(),
    ]