# Generated by Django 3.0.5 on 2020-05-15 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('graph', '0002_auto_20200515_1753'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vertex',
            old_name='plan_object_color',
            new_name='color',
        ),
        migrations.RenameField(
            model_name='vertex',
            old_name='plan_object_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='vertex',
            old_name='plan_object_priority',
            new_name='priority',
        ),
    ]
