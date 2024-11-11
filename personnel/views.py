from django.views.generic import TemplateView, ListView

from . import models


# Create your views here.
class PersonnelHomeView(TemplateView):
    template_name = 'personnel/home.html'
    
class PersonnelListView(ListView):
    model = models.Employee
    template_name = 'personnel/list.html'
    context_object_name = 'employees'
    
    
    