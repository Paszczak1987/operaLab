from django.views.generic import TemplateView


# Create your views here.
class HomeHomeView(TemplateView):
    template_name = 'home/home.html'
