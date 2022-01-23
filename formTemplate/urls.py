from django.urls import path
from .views import formResponseapiView, formsapiview, getFormapiView, formResponseGetapiView
from rest_framework import routers

router = routers.SimpleRouter()
router.register('form', getFormapiView)
router.register('getresponse', formResponseGetapiView, basename='get_response')
urlpatterns = [
    path('', formsapiview.as_view(),name='post_form'),
    path('reponse/', formResponseapiView.as_view(),name='store_response'),
]

urlpatterns += router.urls