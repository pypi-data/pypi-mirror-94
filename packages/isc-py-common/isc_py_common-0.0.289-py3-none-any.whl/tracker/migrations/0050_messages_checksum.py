# Generated by Django 2.2.5 on 2019-09-04 17:48

from django.db import migrations
import isc_common.fields.code_field


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0049_auto_20190903_2155'),
    ]

    operations = [
        migrations.AddField(
            model_name='messages',
            name='checksum',
            field=isc_common.fields.code_field.CodeField(blank=True, null=True),
        ),
    ]
