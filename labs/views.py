from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView

# Create your views here.
from . import models
from . import forms

class LabHomeView(TemplateView):
    template_name = 'labs/home.html'
    
class LabListView(ListView):
    model = models.Laboratory
    template_name = 'labs/list.html'
    context_object_name = 'laboratories'
    
class LabDetailView(DetailView):
    model = models.Laboratory
    template_name = 'labs/detail.html'
    context_object_name = 'lab'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        formatted_address = self.object.formatted_address()
        context['street'] = formatted_address['street']
        context['city'] = formatted_address['city']
        context['country'] = formatted_address['country']
        return context


class LabAddView(CreateView):
    model = models.Laboratory
    form_class = forms.LabAddForm
    template_name = 'labs/add.html'
    success_url = reverse_lazy('labs:list')
