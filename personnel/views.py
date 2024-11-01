from django.views.generic import TemplateView


# Create your views here.
class PersonnelHomeView(TemplateView):
    template_name = 'personnel/home.html'
    
    