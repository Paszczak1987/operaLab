from django.urls import path
from . import views

app_name = 'personnel'

urlpatterns = [
    path('home/', views.PersonnelHomeView.as_view(), name='home'),
    path('list/', views.PersonnelListView.as_view(), name='list'),
    path('technician_view/<int:pk>/', views.PersonnelTechnicianDetailView.as_view(), name='technician_view'),
    path('lab_manager_view/<int:pk>/', views.PersonnelLabManagerDetailView.as_view(), name='lab_manager_view'),
    path('group_manager_view/<int:pk>/', views.PersonnelGroupManagerDetailView.as_view(), name='group_manager_view'),
    path('director_view/<int:pk>/', views.PersonnelDirectorDetailView.as_view(), name='director_view'),
]
