# Generated by Django 4.2.7 on 2023-11-18 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_historicalexpenseline_expenseline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expenseline',
            name='action_item_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='expenseline',
            name='item_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='expenseline',
            name='project_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='historicalexpenseline',
            name='action_item_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='historicalexpenseline',
            name='item_id',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='historicalexpenseline',
            name='project_id',
            field=models.TextField(default=''),
        ),
    ]
