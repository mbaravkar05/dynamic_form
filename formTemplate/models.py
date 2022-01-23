from django.db import models
import uuid
from users.models import User
# Create your models here.

class Form(models.Model):
    form_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    form_name = models.CharField(verbose_name="field name", max_length=500, default=False, unique=True)
    form_description = models.CharField(max_length= 10000,verbose_name="form description",default=False)
    owner = models.ForeignKey(User, on_delete = models.CASCADE ,related_name ="users")
    created_date = models.DateTimeField(auto_now_add=True, blank=False)
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return str(self.form_id)
    
class Fields(models.Model):
    field_id = models.AutoField(primary_key=True)
    field_name = models.CharField(verbose_name="field name", max_length=500, default=False, unique=False)
    field_type = models.CharField(verbose_name="type for field", max_length=250, default=True, unique=False)
    form =  models.ForeignKey(Form, on_delete = models.CASCADE , related_name="form")
    required = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.field_id},{self.field_name}"

    @property
    def choices(self):
        choices = Choices.objects.filter(for_field=self.field_id)
        if choices.exists:
            return choices.values()
        return {} 
    
class Choices(models.Model):
    choice_id = models.AutoField(primary_key=True)
    choice_name = models.CharField(verbose_name="choice name", max_length=500, default=False, unique=False)
    for_field =  models.ForeignKey(Fields, on_delete = models.CASCADE , related_name="fields_choices")
    
    def __str__(self):
        return self.choice_name

class formResponseGroup(models.Model):
    group_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete = models.CASCADE ,related_name ="users_response")
    form_response = models.ForeignKey(Form, on_delete = models.CASCADE ,related_name ="form_Response")
    
    def __str__(self):
        return str(self.group_id)
    
    @property
    def group_data(self):
        group = FieldResponse.objects.filter(response_group=self.group_id)
        return group.values()
    
class FieldResponse(models.Model):
    response = models.CharField(verbose_name="response", max_length=500, default=False, unique=False)
    response_field = models.ForeignKey(Fields, on_delete = models.CASCADE , related_name="fields")
    response_group = models.ForeignKey(formResponseGroup, on_delete = models.CASCADE , related_name="group")
    response_date = models.DateTimeField(auto_now_add=True, blank=False)
    
    def __str__(self):
        return str(self.response)
    
    