# Generated by Django 4.2.7 on 2023-11-08 23:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_historicalexpenseheader_expenseheader'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalExpenseLine',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('UUID', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False)),
                ('division_id', models.IntegerField()),
                ('expense_header_uuid', models.UUIDField()),
                ('line_number', models.IntegerField(db_index=True)),
                ('item_description', models.TextField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=13)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=13)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=13)),
                ('date_required', models.DateTimeField()),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Waiting for Approval', 'Waiting for Approval'), ('Approved', 'Approved'), ('In Process', 'In Process'), ('Closed', 'Closed'), ('Cancelled', 'Cancelled')], max_length=25)),
                ('payment_status', models.CharField(choices=[('Not Paid', 'Not Paid'), ('Ready to be Paid', 'Ready to be Paid'), ('Payment in Process', 'Payment in Process'), ('Paid in Full', 'Paid in Full')], max_length=25)),
                ('Accounting_link', models.JSONField()),
                ('Account_id', models.TextField()),
                ('Instructions', models.JSONField()),
                ('Comments', models.JSONField()),
                ('Tags', models.JSONField()),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('action_item_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.actionitem')),
                ('expense_header_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.expenseheader')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.item')),
                ('project_id', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='api.project')),
            ],
            options={
                'verbose_name': 'historical expense line',
                'verbose_name_plural': 'historical expense lines',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='ExpenseLine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('division_id', models.IntegerField()),
                ('expense_header_uuid', models.UUIDField()),
                ('line_number', models.IntegerField(unique=True)),
                ('item_description', models.TextField()),
                ('quantity', models.DecimalField(decimal_places=2, max_digits=13)),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=13)),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=13)),
                ('date_required', models.DateTimeField()),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Waiting for Approval', 'Waiting for Approval'), ('Approved', 'Approved'), ('In Process', 'In Process'), ('Closed', 'Closed'), ('Cancelled', 'Cancelled')], max_length=25)),
                ('payment_status', models.CharField(choices=[('Not Paid', 'Not Paid'), ('Ready to be Paid', 'Ready to be Paid'), ('Payment in Process', 'Payment in Process'), ('Paid in Full', 'Paid in Full')], max_length=25)),
                ('Accounting_link', models.JSONField()),
                ('Account_id', models.TextField()),
                ('Instructions', models.JSONField()),
                ('Comments', models.JSONField()),
                ('Tags', models.JSONField()),
                ('action_item_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_line_action', to='api.actionitem')),
                ('expense_header_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ExpenseLine_expense_header', to='api.expenseheader')),
                ('item_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ExpenseLine_item', to='api.item')),
                ('project_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='expense_line_project', to='api.project')),
            ],
        ),
    ]
