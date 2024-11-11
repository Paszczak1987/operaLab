from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    path('home/', views.PersonnelHomeView.as_view(), name='home'),
    path('list/', views.PersonnelListView.as_view(), name='list'),
]
