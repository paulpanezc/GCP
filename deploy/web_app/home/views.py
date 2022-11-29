from django.shortcuts import render
from django.views.generic import TemplateView
from ubigeo.models import Departamento

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        departamentos = Departamento.objects.all().order_by('nombre')
        context['departamentos'] = departamentos
        return context
