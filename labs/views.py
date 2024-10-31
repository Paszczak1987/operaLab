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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        laboratories_with_context = []
        for lab in context[self.context_object_name]:
            lab_info = {
                'pk': lab.pk,
                'short_name': lab.short_name,
                'lab_code': lab.lab_code,
                'street': lab.street,
                'number': lab.number,
                'zip_code': lab.zip_code,
                'city': lab.city,
                'country': lab.country,
                'leadership_area': lab.leadership_area,
                'contact_email': lab.contact_email,
                'has_gps_coordinates': lab.has_gps_coordinates(),
                'has_postal_address': lab.has_postal_address(),
                'google_map_url': lab.google_map_url(),
            }
            laboratories_with_context.append(lab_info)
        context['laboratories'] = laboratories_with_context
        return context
        
class LabDetailView(DetailView):
    model = models.Laboratory
    template_name = 'labs/detail.html'
    context_object_name = 'lab'

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
    