from django.views.generic import TemplateView, ListView, DetailView

from . import models


# Create your views here.
class PersonnelHomeView(TemplateView):
    template_name = 'personnel/home.html'


class PersonnelListView(ListView):
    model = models.Employee
    template_name = 'personnel/list.html'
    context_object_name = 'employees'


class PersonnelTechnicianDetailView(DetailView):
    model = models.Technician
    template_name = 'personnel/detail.html'
    context_object_name = 'emp'


class PersonnelLabManagerDetailView(DetailView):
    model = models.LabManager
    template_name = 'personnel/detail.html'
    context_object_name = 'emp'


class PersonnelGroupManagerDetailView(DetailView):
    model = models.GroupManager
    template_name = 'personnel/detail.html'
    context_object_name = 'emp'


class PersonnelDirectorDetailView(DetailView):
    model = models.Director
    template_name = 'personnel/detail.html'
    context_object_name = 'emp'
