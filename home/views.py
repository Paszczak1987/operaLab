from django.views.generic import TemplateView
from django.shortcuts import render

# Create your views here.
class HomeHomeView(TemplateView):
    template_name = 'home/home.html'

