# Generated by Django 3.0.5 on 2020-06-03 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0003_auto_20200515_1902'),
    ]

    operations = [
        migrations.AddField(
            model_name='edge',
            name='library_id',
            field=models.CharField(default=None, max_length=200),
        ),
    ]
