# Generated by Django 4.2.7 on 2023-11-18 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_expenseline_action_item_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ActionItem',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
        migrations.DeleteModel(
            name='Project',
        ),
    ]