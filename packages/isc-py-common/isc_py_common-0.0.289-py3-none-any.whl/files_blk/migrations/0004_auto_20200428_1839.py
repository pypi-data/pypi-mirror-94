# Generated by Django 2.2.12 on 2020-04-28 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files_blk', '0003_files_file_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='files',
            name='file_size',
            field=models.PositiveIntegerField(),
        ),
    ]
