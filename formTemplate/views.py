from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import FormResponseSerialiser, FormSerialiser
from rest_framework import mixins, viewsets
import pandas as pd
from datetime import datetime
from django_filters.rest_framework import DjangoFilterBackend

from formTemplate.models import FieldResponse, Form, Fields, Choices, formResponseGroup

class getFormapiView(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """ 
    Get all the form / form filter by the form_id and user_id
    """
    permission_classes = [IsAuthenticated,]
    queryset = Fields.objects.filter(form__status=True)
    serializer_class = FormSerialiser
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['form__owner','form']
    
class formsapiview(APIView):
    permission_classes = [IsAuthenticated,]
    
    def delete(self, request):
        """ 
        To delete the form only deleted by owner
        """
        try:
            form_id = request.query_params.get('form_id')
            form = Form.objects.filter(form_id=form_id, owner=request.user)
            if form:
                form.update(status=False)
                return Response({"success":True, "message":"form deleted succefully", "status":200}, 200)
            return Response({"success":True, "message":"No data found.", "status":200}, 200)
        except Exception as e:
            return Response({"success":False, "message":f"something went wrong.. {e}",  "status":500 },500)

    def post(self,request, *args, **kwargs):
        """
        create form with fields using csv
        """
        try:
            print(request.user)
            data = request.data
            file = pd.read_csv(data.get('form_file'))
            form_name = data.get("form_name")
            form_description = data.get("form_description")
            form = Form.objects.create(form_name=form_name, form_description=form_description, owner=request.user)
            form.save()
            for index,row in file.iterrows():
                if row['type'] == 'singleselect':
                    field = Fields.objects.create(field_name=row['field_name'], field_type=row['type'], \
                        required=row['mandatory'], form=form)
                    field.save()
                    [Choices.objects.create(choice_name=opt, for_field=field).save() for opt in row['options'].split(",")]
                else:
                    field = Fields.objects.create(field_name=row['field_name'], field_type=row['type'], \
                        required=row['mandatory'], form=form)
                    field.save()
            return Response({"success":True, "message":"form created for given csv successfully.", "status":201}, 201)
        except Exception as e:
            return Response({"success":False, "message":f"something went wrong.. {e}",  "status":500 },500)

class formResponseGetapiView(mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated,]
    queryset = formResponseGroup.objects.filter(form_response__status=True)
    serializer_class = FormResponseSerialiser
    filter_backends = [DjangoFilterBackend,]
    filterset_fields = ['group_id','form_response__owner',]
       

class formResponseapiView(APIView):
    permission_classes = [IsAuthenticated,]
    
    def check_type(self, value, type):
        if type == "number" and isinstance(value, (int, float)):
            return True
        if type == "date" and datetime.strptime(value,"%d/%m/%Y"):
            return True
        if type == "text" and isinstance(value, str):
            return True
        if type == "singleselect":
            return True
    
    
    def post(self, request):
        """
        store form response for form fields
        """
        try:
            form_id = request.data.get("form_id")
            data = request.data.get("data")
            form = Form.objects.filter(form_id=form_id, status=True)
            if form:
                group_ = formResponseGroup.objects.create(user_id=request.user,form_response_id=form_id)
                for field in data:
                    field_id = field.get('field_id') 
                    response = field.get('response')
                    type = field.get("type")
                    if self.check_type(response, type):
                        field_response = FieldResponse.objects.create(response=response, response_field_id=field_id,\
                            response_group=group_)
                        field_response.save()
                    else:
                        return Response({"success":False, "message":"Please check type of field.",  "status":500 },500)    
                return Response({"success":True, "message":"Your reponse stored succefully.",  "status":201 },201)    
            else:
                return Response({"success":False, "message":"Sorry, Form is not active.",  "status":204 },204)    
        except Exception as e:
            return Response({"success":False, "message":f"something went wrong.. {e}",  "status":500 },500)

