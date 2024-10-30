from django.urls import path
from . import views

app_name = 'labs'
urlpatterns = [
    path('home/', views.LabHomeView.as_view(), name='home'),
    path('list/', views.LabListView.as_view(), name='list'),
    path('add/', views.LabAddView.as_view(), name='add'),
    # path('edit/<int:id>/', views.labs_edit, name='labs_edit'),
    # path('delete/<int:id>/', views.labs_delete, name='labs_delete'),
    path('detail_view/<int:pk>/', views.LabDetailView.as_view(), name='detail_view'),
]
