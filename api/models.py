from django.db import models
from django.contrib.auth.models import AbstractUser
from . import macros
from simple_history.models import HistoricalRecords
from .manager import SoftDeleteManager

import uuid

# Create your models here.
class User(AbstractUser):
    usertype = models.CharField(max_length=9, choices=macros.USER_TYPE)

# class Item(models.Model):
#     description=models.CharField(max_length=20)

# class ActionItem(models.Model):
#     name=models.CharField(max_length=20)

# class Project(models.Model):
#     name=models.CharField(max_length=20)

class ExpenseHeader(models.Model):
    UUID=models.UUIDField(default = uuid.uuid4,editable = False,unique=True)
    division_id=models.IntegerField()
    vendor_location_id=models.IntegerField()
    terms_id=models.IntegerField()
    name=models.CharField(max_length=64)
    status=models.CharField(max_length=25,choices=macros.STATUS)
    type=models.CharField(max_length=20,choices=macros.EXPENSE_TYPE)
    issue_date=models.DateTimeField(null=True)  #auto-generated when status=Approved
    accounting_link=models.JSONField()
    tags=models.JSONField(null=True)
    created_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='creator',null=True)    #refers to user that created the Expense_header
    created_at=models.DateTimeField(auto_now_add=True)  #auto-generated when this expense_header is created
    updated_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='updator',null=True)    #refers to user that updated the Expense_header
    updated_at=models.DateTimeField(auto_now=True)  #auto-generated when this expense_header is updated
    deleted_by=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='deletor',null=True)

    objects=SoftDeleteManager()
    all_objects=models.Manager()
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        # Check if the status is changing to 'Approved' and the issue_date is not set
        if self.status == 'Approved' and not self.issue_date:
            from django.utils import timezone
            self.issue_date = timezone.now()

        super().save(*args, **kwargs)

class ExpenseLine(models.Model):
    UUID=models.UUIDField(default = uuid.uuid4,editable = False,unique=True)
    division_id=models.IntegerField()   #set automaticaly from the division_id of the expense_header in expense_header_id
    project_id=models.TextField(default="") 
    action_item_id=models.TextField(default="")    
    expense_header_id=models.ForeignKey(ExpenseHeader,on_delete=models.SET_NULL,related_name='ExpenseLine_expense_header',null=True)    #refers to an expense_header,set automaticaly from the expense_header.UUId
    expense_header_uuid=models.UUIDField(max_length=100)    #set automaticaly from the expense_header_id.UUId
    line_number=models.IntegerField(unique=True)    #generated automaticaly in increamental order
    item_id=models.TextField(default="")
    item_description=models.TextField() #set automatical from item_id.description
    quantity=models.DecimalField(max_digits=13,decimal_places=2)
    unit_price=models.DecimalField(max_digits=13,decimal_places=2)
    total_price=models.DecimalField(max_digits=13,decimal_places=2) #calculated automaticaly from quantity and unit_price
    date_required=models.DateTimeField()
    status=models.CharField(max_length=25,choices=macros.STATUS) #set automaticaly from expense_header_id.status
    payment_status=models.CharField(max_length=25,choices=macros.PAYMENT_STATUS)
    Accounting_link=models.JSONField()
    Account_id=models.TextField()
    Instructions=models.JSONField()
    Comments=models.JSONField()
    Tags=models.JSONField()

    history=HistoricalRecords()

    #overiding default save method
    def save(self,*args,**kwargs):
        self.expense_header_id=ExpenseHeader.objects.get(UUID=self.expense_header_uuid)   #get expense_header_id from the expense_header_uuid given
        self.item_description=""  #Item Description as Empty String
        #self.division_id=self.expense_header_id.division_id #obtain division_id from expense_header_id.division_id
        self.total_price=self.quantity*self.unit_price  #calculate total price

        #auto-generating line_number
        if not self.line_number:
            last_line = ExpenseLine.objects.order_by('-line_number').first()
            if last_line:
                self.line_number = last_line.line_number + 1
            else:
                self.line_number = 1
        super().save(*args, **kwargs)
