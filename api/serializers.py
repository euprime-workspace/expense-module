from rest_framework import serializers
from simple_history.utils import update_change_reason
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'usertype']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name']

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['description']

class ActionItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionItem
        fields = ['name']

class ExpenseHeaderSerializer(serializers.ModelSerializer):
    change_reason = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = ExpenseHeader
        exclude = ['id']  # Not part of GET method's response
        read_only_fields = ['issue_date', 'created_by', 'created_at', 'updated_by', 'updated_at',
                            'deleted_by']  # Updated according to criteria by backend and can't be updated by POST request

    def create(self, validated_data):
        # Check if the request data is a list
        if isinstance(validated_data, list):
            # Create and return a list of ExpenseHeader instances
            change_reason = validated_data.pop('change_reason', '')
            instances = [ExpenseHeader.objects.create(**item) for item in validated_data]
            if change_reason:
                for instance in instances:
                    update_change_reason(instance, change_reason)
            return instances
        else:
            # Remove 'change_reason' from validated_data as it's not part of the model fields
            change_reason = validated_data.pop('change_reason', ' ')

            # Create and return a single ExpenseHeader instance
            instance = ExpenseHeader.objects.create(**validated_data)

            # Update the change reason if provided
            # print("SSchange_reason: ",change_reason)
            if change_reason:
                update_change_reason(instance, change_reason)

            return instance

    def update(self, instance, validated_data):
        # Update the change reason if provided in the request data
        change_reason = validated_data.pop('change_reason', '')  # Remove change_reason from validated_data
        instance = super().update(instance, validated_data)
        update_change_reason(instance, change_reason)  # Update the change reason
        # instance.save()
        return instance

    def delete(self, instance, deleted_by):
        instance.deleted_by = deleted_by
        print(deleted_by)
        instance.save()

class ExpenseLineSerializer(serializers.ModelSerializer):
    # division_id = serializers.IntegerField(required=False)  #Not required in POST request
    class Meta:
        model = ExpenseLine
        exclude = ['id', 'expense_header_id']  # Not included in GET response
        read_only_fields = ['item_description', 'expense_header_id', 'total_price',
                            'line_number']  # Updated according to criteria by backend and can't be updated by POST request

class HistoricalExpenseHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalExpenseHeader  # Use the HistoricalRecord model
        fields = '__all__'

class HistoricalExpenseLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalExpenseLine
        fields = '__all__'
