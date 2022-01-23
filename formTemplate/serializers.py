from .models import Fields, FieldResponse, formResponseGroup
from rest_framework import serializers

class FormSerialiser(serializers.ModelSerializer):
    form_name = serializers.ReadOnlyField(source='form.form_name')
    form_description = serializers.ReadOnlyField(source='form.form_description')
    form_id = serializers.ReadOnlyField(source='form.form_id')
    form_owner = serializers.ReadOnlyField(source='form.owner.id')
    
    class Meta:
        model = Fields
        fields = ( 'choices','field_name', 'field_id','field_type', 'required', 'form_name', 'form_description', 'form_id','form_owner')
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if not getattr(instance, attr):
                setattr(instance, attr, value)
        instance.save()
        return instance 

class FormResponseSerialiser(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user_id.email')
    user_id = serializers.ReadOnlyField(source='user_id.id')
    form_name = serializers.ReadOnlyField(source='form_response.form_name')
    form_description = serializers.ReadOnlyField(source='form_response.form_description')
    form_id = serializers.ReadOnlyField(source='form_response.form_id')
    form_owner = serializers.ReadOnlyField(source='form_response.owner.id')
    
    class Meta:
        model = formResponseGroup
        fields = ('group_data','user',"user_id",'form_name','form_description', 'form_id', 'form_owner')