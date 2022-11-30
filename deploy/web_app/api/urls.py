from django.urls import path
from . import views

urlpatterns = [
    path('distrito/<int:distrito_id>', views.API().get_distrito, name='distrito'),
    path('distritos/<int:provincia_id>', views.API().get_distritos, name='distritos'),
    path('prediction', views.API().prediction, name='prediction'),
    path('provincias/<int:departamento_id>', views.API().get_provincias, name='provincias'),
    path('ubigeo', views.API().ubigeo, name='ubigeo'),
]