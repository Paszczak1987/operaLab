from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, TemplateView, CreateView, UpdateView
from django.db import IntegrityError

from . import models
from . import forms

# Create your views here.
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
        address = self.object.formatted_address()
        context['street'] = address['street']
        context['number'] = address['number']
        context['zip_code'] = address['zip_code']
        context['city'] = address['city']
        context['country'] = address['country']
        return context

class LabAddView(CreateView):
    model = models.Laboratory
    form_class = forms.LabAddForm
    template_name = 'labs/add.html'
    success_url = reverse_lazy('labs:list')
    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError as e:
            if 'name' in str(e):
                form.add_error('name', 'Lab with this name already exists.')
            if 'short_name' in str(e):
                form.add_error('short_name', 'Lab with this short name already exists.')
            if 'lab_code' in str(e):
                form.add_error('lab_code', 'Lab with this code already exists.')
            return self.form_invalid(form)
        

class LabEditView(UpdateView):
    model = models.Laboratory
    form_class = forms.LabAddForm
    template_name = 'labs/edit.html'
    success_url = reverse_lazy('labs:list')
    context_object_name = 'lab'
    